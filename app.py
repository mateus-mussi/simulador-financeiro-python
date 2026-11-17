from flask import Flask, request, render_template
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as Dcb
from bcb import sgs
import plotly.express as Px
import pandas as pd
import yfinance as yf
from openpyxl import load_workbook
from flask import Flask, request, send_file, redirect, url_for
from io import BytesIO
from pathlib import Path
import os
import bd  # Importando o arquivo bd.py



app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

#Investimento
app_dash = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix="/dash/",
    external_stylesheets=[Dcb.themes.DARKLY]
)

def DadosInvestimento(CapitalInicial, DataInicio, DataFim, Frequencia, Risco, InvestimentoMensal):
    """Simula saldo nominal com taxas diárias e aportes mensais.

    Aportes ocorrem em cada aniversário mensal após a data inicial. A escolha
    do gráfico (diário/mensal/anual) não altera os cálculos.
    Retorno: (série para o gráfico, total aportado, lucro nominal).
    """
    inicio = pd.Timestamp(DataInicio).normalize()
    fim = pd.Timestamp(DataFim).normalize()
    if inicio >= fim:
        raise ValueError("A data final deve ser posterior à data inicial.")
    if CapitalInicial is None or InvestimentoMensal is None:
        raise ValueError("Informe o capital inicial e o aporte mensal.")
    capital_inicial = float(CapitalInicial)
    aporte = float(InvestimentoMensal)
    if not all(pd.notna(x) and x >= 0 and x != float("inf") for x in (capital_inicial, aporte)):
        raise ValueError("Capital inicial e aporte devem ser valores finitos não negativos.")
    if Frequencia not in ("D", "M", "Y"):
        raise ValueError("Frequência inválida.")

    if Risco in ("Baixo", "Médio", "CDI (110%)"):
        taxas = sgs.get({"SELIC": 11, "CDI": 12}, start=inicio, end=fim)
        if taxas is None or taxas.empty:
            raise ValueError("Não foram encontradas taxas SELIC/CDI para o período.")
        coluna = "SELIC" if Risco == "Baixo" else "CDI"
        multiplicador = 1.0 if Risco == "Baixo" else (1.2 if Risco == "Médio" else 1.1)
        # BCB SGS 11/12: percentual diário; não é taxa mensal.
        variacoes = pd.to_numeric(taxas[coluna], errors="coerce").dropna() / 100 * multiplicador
    elif Risco == "Alto":
        historico = yf.download(
            "BTC-USD", start=inicio, end=fim + pd.Timedelta(days=1),
            auto_adjust=True, progress=False
        )
        if historico is None or historico.empty:
            raise ValueError("Não foram encontradas cotações de Bitcoin para o período.")
        # yfinance pode retornar colunas MultiIndex mesmo para um único ticker.
        fechamento = historico["Close"]
        if isinstance(fechamento, pd.DataFrame):
            fechamento = fechamento.iloc[:, 0]
        fechamento = pd.to_numeric(fechamento, errors="coerce").dropna()
        if fechamento.empty:
            raise ValueError("Não foram encontradas cotações válidas de Bitcoin.")
        variacoes = fechamento.pct_change().fillna(0.0)
    else:
        raise ValueError("Tipo de investimento inválido.")

    variacoes.index = pd.DatetimeIndex(pd.to_datetime(variacoes.index)).tz_localize(None).normalize()
    variacoes = variacoes[~variacoes.index.duplicated(keep="last")].sort_index()
    dias = pd.date_range(inicio, fim, freq="D")
    variacoes = variacoes.reindex(dias, fill_value=0.0)

    meses = 1
    datas_aportes = set()
    while True:
        data_aporte = inicio + pd.DateOffset(months=meses)
        if data_aporte > fim:
            break
        datas_aportes.add(data_aporte)
        meses += 1

    saldo = capital_inicial
    aportes_realizados = 0
    trajetoria = {inicio: saldo}
    for dia in dias[1:]:
        saldo *= 1.0 + float(variacoes.loc[dia])
        if dia in datas_aportes:
            saldo += aporte
            aportes_realizados += 1
        trajetoria[dia] = saldo

    serie = pd.Series(trajetoria, dtype="float64")
    if Frequencia == "D":
        exibicao = serie
    else:
        periodo = "M" if Frequencia == "M" else "Y"
        exibicao = serie.groupby(serie.index.to_period(periodo)).tail(1)
    total_investido = capital_inicial + aporte * aportes_realizados
    lucro_nominal = saldo - total_investido
    return exibicao, total_investido, lucro_nominal

navbar = html.Nav(
    children=[
        html.Ul(
            children=[
                html.Li(html.A("Home", href="/", style={'color': 'white', 'textDecoration': 'none', 'padding': '20px'})),
                html.Li(html.A("Investimentos", href="/dash/", style={'color': 'white', 'textDecoration': 'none', 'padding': '20px'})),
                html.Li(html.A("Holerite", href="/holerite", style={'color': 'white', 'textDecoration': 'none', 'padding': '20px'})),
                html.Li(html.A("Monitoramento de Gastos", href="/gastos", style={'color': 'white', 'textDecoration': 'none', 'padding': '2  0px'})),
            ],
            style={'display': 'flex', 'listStyle': 'none', 'justifyContent': 'center', 'background': '#333', 'margin': 0}
        )
    ]
)

app_dash.layout = html.Div([ 
    navbar,  # Adiciona o navbar no layout
    Dcb.Container([  # Aqui está o Container, onde você pode usar fluid=True
        Dcb.Row([  # Criei uma linha que contém duas colunas
            Dcb.Col([ 
                html.H1("Parâmetros de Entrada", style={'font-weight': 'bold', 'color': 'lightblue'}),
                Dcb.Row([ 
                    Dcb.Col([ 
                        Dcb.Label("Capital Inicial"), 
                        Dcb.Input(id="CapitalInicial", placeholder="Capital Inicial", type="number", value=1000), 
                    ]) 
                ], className="mb-2"), 
                Dcb.Row([ 
                    Dcb.Col([ 
                        Dcb.Label("Investimento Mensal"), 
                        Dcb.Input(id="InvestimentoMensal", placeholder="Investimento Mensal", type="number", value=0), 
                    ]) 
                ], className="mb-2"), 
                Dcb.Row([ 
                    Dcb.Col([ 
                        Dcb.Label("Data Início"), 
                    ], width='auto'), 
                    Dcb.Col([ 
                        dcc.DatePickerSingle(id="DataInicio", date="2020-01-01", display_format='YYYY-MM-DD'), 
                    ]) 
                ], className="mb-3"), 
                Dcb.Row([ 
                    Dcb.Col([ 
                        Dcb.Label("Data de Fim"), 
                    ], width='auto'), 
                    Dcb.Col([ 
                        dcc.DatePickerSingle(id="DataFim", date="2024-01-01", display_format='YYYY-MM-DD'), 
                    ]) 
                ], className="mb-3"), 
                Dcb.Row([ 
                    Dcb.Col([ 
                        Dcb.Label("Frequência"), 
                        Dcb.Select( 
                            id="Frequencia", 
                            options=[ 
                                {'label': 'Dia', 'value': 'D'}, 
                                {'label': 'Mês', 'value': 'M'}, 
                                {'label': 'Ano', 'value': 'Y'} 
                            ], 
                            value='M', 
                        ), 
                    ]) 
                ], className="mb-2"), 
                Dcb.Row([ 
                    Dcb.Col([ 
                        Dcb.Label("Tipo de Investimento"), 
                        Dcb.Select( 
                            id="TipoRisco", 
                            options=[ 
                                {'label': 'Baixo (SELIC)', 'value': 'Baixo'}, 
                                {'label': 'Médio (CDB)', 'value': 'Médio'}, 
                                {'label': 'Alto (Bitcoin)', 'value': 'Alto'}, 
                                {'label': 'CDI (110%)', 'value': 'CDI (110%)'} 
                            ], 
                            value='Baixo', 
                        ), 
                    ]) 
                ], className="mb-2"), 
                Dcb.Button("Calcular", id="CalcularButton", color="primary", className="mt-2"), 
                html.Div(id="ResumoInvestimento", className="mt-3")  # Div para mostrar o total investido e lucro
            ], width=4, className="border p-3 bf-dark text-white"), 
            
            Dcb.Col([  # Tabela e gráfico ficam lado a lado nesta coluna
                dcc.Graph(id="GraficoLucro"), 
                html.Div(id="TabelaLucro", className="mt-3") 
            ], width=8, className="border p-3 bf-dark text-white") 
        ], className="mt-3")
    ], fluid=True)  # Aqui você pode usar fluid=True dentro do Container
])

def AjustarPorInflacao(Capital, DataInicio, DataFim):
    """Deflaciona o saldo final pela variação composta do IPCA disponível.

    O resultado é o capital final em poder de compra aproximado da data inicial,
    NÃO o lucro real da aplicação (que exigiria deflacionar cada aporte).
    """
    ipca = sgs.get({"IPCA": 433}, start=DataInicio, end=DataFim)
    if ipca is None or ipca.empty:
        raise ValueError("Não foram encontrados dados de IPCA para o período.")
    taxas_mensais = pd.to_numeric(ipca["IPCA"], errors="coerce").dropna()
    if taxas_mensais.empty:
        raise ValueError("Não foram encontrados valores válidos de IPCA.")
    fator = float((1 + taxas_mensais / 100).prod())
    if fator <= 0:
        raise ValueError("Índice acumulado de inflação inválido.")
    return float(Capital) / fator, (fator - 1) * 100

@app_dash.callback(      
    [Output("GraficoLucro", "figure"),
     Output("TabelaLucro", "children"),
     Output("ResumoInvestimento", "children")],  
    [Input("CapitalInicial", "value"),
     Input("InvestimentoMensal", "value"),
     Input("DataInicio", "date"),
     Input("DataFim", "date"),
     Input("Frequencia", "value"),
     Input("TipoRisco", "value"),
     Input("CalcularButton", "n_clicks")]
)
def AtualizarGraficoETabela(CapitalInicial, InvestimentoMensal, DataInicio, DataFim, Frequencia, TipoRisco, NClicks):
    # Se o botão não foi clicado, retorne dash.no_update para todos os outputs
    if not NClicks:
        return dash.no_update, dash.no_update, dash.no_update
    
    DataInicio = pd.to_datetime(DataInicio)
    DataFim = pd.to_datetime(DataFim)
    
    SerieLucros, TotalInvestido, Lucro = DadosInvestimento(CapitalInicial, DataInicio, DataFim, Frequencia, TipoRisco, InvestimentoMensal)
    SerieLucros = SerieLucros.reset_index()
    SerieLucros.columns = ["Data", "LucroAcumulado"]
    SerieLucros["LucroAcumulado"] = SerieLucros["LucroAcumulado"].round(2)
    SerieLucros["Data"] = SerieLucros["Data"].dt.date
    
    # Calcular o Lucro Real ajustado pela inflação
    CapitalReal, Inflacao = AjustarPorInflacao(SerieLucros['LucroAcumulado'].iloc[-1], DataInicio, DataFim)
    
    Fig = Px.line(SerieLucros, x="Data", y="LucroAcumulado", title=f"Lucro Acumulado ({TipoRisco} Risco)")
    
    Tabela = dash_table.DataTable(
        data=SerieLucros.to_dict('records'),
        columns=[{"name": i, "id": i} for i in ['Data', 'LucroAcumulado']],
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'textAlign': 'center'},
        style_data={'color': 'black', 'backgroundColor': 'white', 'textAlign': 'center'},
        style_table={'maxHeight': '400px', 'overflowY': 'scroll'}
    )
    
    # Resumo com o Lucro Real ajustado pela inflação
    Resumo = html.Div([
        html.H1("Resumo do Investimento", style={'font-weight': 'bold', 'color': 'lightblue'}),
        html.H5(f"Total Investido: R$ {TotalInvestido:.2f}", style={'font-weight': 'bold', 'color': 'lightgreen'}),
        html.H5(f"Lucro: R$ {Lucro:.2f}", style={'font-weight': 'bold', 'color': 'orange'}),
        html.H5(f"Total (Investido + Lucro): R$ {TotalInvestido + Lucro:.2f}", style={'font-weight': 'bold', 'color': 'purple'}),
        html.H5(f"Capital final ajustado pelo IPCA (aprox.): R$ {CapitalReal:.2f}", style={'font-weight': 'bold', 'color': 'red'}),
        html.H5(f"IPCA acumulado disponível no período: {Inflacao:.2f}%", style={'font-weight': 'bold', 'color': 'white'}),
    ], style={'margin-top': '20px'})

    return Fig, Tabela, Resumo

#Holerite

# Função para processar os dados e salvar no Excel
def processar_arquivo_excel(nome_empresa, cnpj_empresa, data_holerite, matricula, nome_funcionario, salario, cargo, admissao, beneficios, descontos):
    # Abrir o arquivo Excel
    wb = load_workbook(Path(__file__).with_name('holerite_modelo.xlsx'))
    aba_holerite = wb["contracheque"]  
    
    # Atualizar informações da empresa
    aba_holerite['C3'] = nome_empresa
    aba_holerite['D5'] = cnpj_empresa
    aba_holerite['G5'] = data_holerite
    
    # Atualizar informações do funcionário
    aba_holerite['C8'] = matricula
    aba_holerite['D8'] = nome_funcionario
    aba_holerite['H14'] = salario
    aba_holerite['H7'] = cargo
    aba_holerite['C10'] = admissao
    
    # Atualizar os benefícios
    linha_beneficio = 15  # Linha inicial para benefícios
    for beneficio in beneficios:
        aba_holerite[f'D{linha_beneficio}'] = beneficio['nome_beneficio']
        aba_holerite[f'H{linha_beneficio}'] = beneficio['vencimento']
        linha_beneficio += 1
    
    # Atualizar os descontos
    linha_desconto = linha_beneficio + 2  # Deixe espaço entre benefícios e descontos
    for desconto in descontos:
        aba_holerite[f'D{linha_desconto}'] = desconto['nome_desconto']        
        aba_holerite[f'K{linha_desconto}'] = desconto['desconto'] 
        linha_desconto += 1
    
    # Salvar o arquivo atualizado
    arquivo_saida = BytesIO()
    wb.save(arquivo_saida)
    arquivo_saida.seek(0)
    return arquivo_saida

# Rota para exibir o formulário
@app.route('/holerite', methods=['GET'])
def holerite():
    return render_template('holerite.html')

# Rota para processar o formulário
@app.route('/processar_holerite', methods=['POST'])
def processar_holerite():
    # Receber dados do formulário
    nome_empresa = request.form['nome_empresa']
    cnpj_empresa = request.form['cnpj_empresa']
    data_holerite = request.form['data_holerite']
    matricula = request.form['matricula']
    nome_funcionario = request.form['nome_funcionario']
    salario = float(request.form['salario']) if request.form['salario'].strip() else 0.0
    cargo = request.form['cargo']
    admissao = request.form['admissao']
    
    # Processar os benefícios
    beneficios = []
    for i in range(1, 11):  # Até 10 benefícios
        nome_beneficio = request.form.get(f'nome_beneficio_{i}')
        vencimento = request.form.get(f'vencimento_{i}')
        if nome_beneficio:
            beneficios.append({'nome_beneficio': nome_beneficio, 'vencimento': vencimento})
    
    # Processar os descontos
    descontos = []
    for i in range(1, 11):  # Até 10 descontos
        nome_desconto = request.form.get(f'nome_desconto{i}')
        desconto = request.form.get(f'desconto_{i}')
        if nome_desconto:
            descontos.append({'nome_desconto': nome_desconto, 'desconto': desconto})
    
    # Processar o arquivo Excel
    planilha = processar_arquivo_excel(nome_empresa, cnpj_empresa, data_holerite, matricula, nome_funcionario, salario, cargo, admissao, beneficios, descontos)
    return send_file(planilha, as_attachment=True, download_name='holerite-preenchido.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


#Monitoramento Financeiro

@app.route('/gastos', methods=['GET'])
def mostrar_gastos():
    # Renderiza o arquivo gastos.html
    return render_template('gastos.html')

@app.route('/salvar_receitas',  methods=['GET', 'POST'])
def salvar_receitas():
    # Capturando todos os campos do formulário
    dados_receitas = {}
    
    for key in request.form:
        dados_receitas[key] = request.form[key]

    # Chama a função salvar_no_bd para salvar os dados no banco
    bd.salvar_no_bd(dados_receitas)

    # Após salvar as receitas, redireciona para a página de monitoramento
    return redirect(url_for('mostrar_monitoramento'))

@app.route('/monitoramento', methods=['GET'])
def mostrar_monitoramento():
    ## Pega os dados diretamente do banco/arquivo (chama a função do bd.py)
    dados = bd.obter_dados()
    
    # Calculando os totais
    total_receitas = sum(dados['RECEITAS'].values())
    total_despesas_fixas = sum(dados['DESPESAS FIXAS'].values())
    saldo = total_receitas - total_despesas_fixas

    # Passando os dados para o template
    return render_template('monitoramento.html', dados=dados, total_receitas=total_receitas, total_despesas_fixas=total_despesas_fixas, saldo=saldo)

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1", host="127.0.0.1")