# Simulador Financeiro em Python 📊

Este é um dos projetos que mais quero desenvolver no meu GitHub. Ele começou como um trabalho em equipe e reúne algumas áreas que gosto de estudar: **Python, desenvolvimento web, análise de dados e integração com APIs**.

A proposta é ter um lugar para **simular investimentos, visualizar gráficos, organizar receitas e despesas** e explorar a geração de um holerite demonstrativo.

## 💡 O que o projeto faz

| Módulo | O que encontro nele |
|---|---|
| **Simulador de investimentos** | Simulação de valores aplicados, aportes mensais e gráficos de evolução |
| **Controle de gastos** | Formulário para registrar receitas e despesas por categoria |
| **Monitoramento** | Resumo das informações preenchidas na sessão |
| **Holerite** | Geração de uma planilha Excel fictícia, para fins de demonstração |

O simulador trabalha com séries de **SELIC, CDI e IPCA** e pode consultar cotações históricas de **Bitcoin**. As consultas dependem de serviços externos. **Os resultados são experimentais e não devem ser utilizados como orientação financeira.**

## 🛠️ Tecnologias que usei

- **Python e Flask** para a aplicação web e suas rotas;
- **Dash e Plotly** para o painel e os gráficos;
- **Pandas** para trabalhar com datas e séries financeiras;
- **python-bcb** para consultar indicadores do Banco Central;
- **yfinance** para consultar dados históricos de mercado;
- **openpyxl** para criar e preencher planilhas Excel;
- **HTML e CSS** para as páginas e os estilos.

## 📸 Visual do projeto

![Página inicial do Simulador Financeiro](docs/pagina-inicial.png)

Essa imagem é uma prévia demonstrativa. Para conferir capturas feitas com o aplicativo aberto em um navegador, deixei também os [registros do teste visual](https://github.com/mateus-mussi/simulador-financeiro-python/actions/runs/44014061702).

## ▶️ Como executar no computador

**Requisitos:** Python 3.11, pip e internet para as consultas financeiras.

Clone o repositório e entre na pasta:

```bash
git clone https://github.com/mateus-mussi/simulador-financeiro-python.git
cd simulador-financeiro-python
python -m venv .venv
```

Ative o ambiente virtual.

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

Instale as dependências, prepare a planilha fictícia e inicie o programa:

```bash
python -m pip install -r requirements.txt
python scripts/criar_holerite_modelo.py
python app.py
```

Com o servidor iniciado, acesse:

| Página | Endereço local |
|---|---|
| Início | [http://127.0.0.1:5000](http://127.0.0.1:5000) |
| Simulador | [http://127.0.0.1:5000/dash/](http://127.0.0.1:5000/dash/) |
| Holerite | [http://127.0.0.1:5000/holerite](http://127.0.0.1:5000/holerite) |
| Gastos | [http://127.0.0.1:5000/gastos](http://127.0.0.1:5000/gastos) |
| Monitoramento | [http://127.0.0.1:5000/monitoramento](http://127.0.0.1:5000/monitoramento) |

O modelo de holerite criado pelo script contém apenas dados fictícios. **Não utilizo esse módulo para emitir documentos trabalhistas oficiais.**

## 🧪 Como estou testando

Quis ir além de publicar os arquivos: comecei a incluir testes para descobrir problemas e evitar que correções anteriores se percam.

Para executar os testes:

```bash
python -m unittest discover -s tests -v
```

Também configurei o **GitHub Actions**, que instala as dependências e executa automaticamente os testes:

- [Ver os testes do Python, Flask e Dash](https://github.com/mateus-mussi/simulador-financeiro-python/actions/runs/44013703245): **15 testes aprovados**, usando dados financeiros simulados.
- [Ver a navegação testada no Chromium](https://github.com/mateus-mussi/simulador-financeiro-python/actions/runs/44014061702): as **cinco páginas principais abriram corretamente**, e o navegador gerou capturas de tela.

Esses resultados me ajudam a acompanhar a qualidade do código, mas ainda quero testar os cálculos com **séries históricas reais** e verificar melhor o comportamento das APIs.

## 📈 Como funciona a simulação

Na lógica atual, os aportes entram mensalmente e não mudam quando escolho exibir o gráfico por dia, mês ou ano. As taxas das séries SELIC/CDI são aplicadas nos dias correspondentes, e o IPCA é acumulado por composição.

Alguns detalhes importantes:

- A opção de CDB é **hipotética** e usa um multiplicador do CDI, sem reproduzir impostos, tarifas ou regras de um produto real.
- A simulação de Bitcoin utiliza variações de preços históricos e não considera custos de negociação.
- O valor ajustado pelo IPCA representa uma aproximação do poder de compra do saldo final. **Não é o lucro real dos aportes realizados ao longo do tempo.**
- O controle de despesas ainda guarda os valores apenas temporariamente: **não possui banco de dados persistente**.

## 📁 Organização

```text
simulador-financeiro-python/
├── app.py
├── bd.py
├── requirements.txt
├── templates/
├── static/
│   ├── css/
│   └── images/
├── scripts/
│   ├── criar_holerite_modelo.py
│   └── validar_navegador.py
├── tests/
│   ├── test_aportes.py
│   ├── test_bd.py
│   ├── test_modelo_financeiro.py
│   └── test_web.py
├── docs/
└── README.md
```

## 🔧 Próximos passos

Quero revisar as respostas das APIs quando não houver dados ou a conexão falhar, conferir a precisão de mais cenários financeiros e melhorar a experiência nas telas. Também pretendo estudar uma maneira de salvar os lançamentos de gastos de forma persistente.

Mantenho uma [lista de tarefas e verificações técnicas](docs/PENDENCIAS.md) para acompanhar esses pontos.

## 👥 Desenvolvimento em equipe

Este projeto foi desenvolvido em grupo por **Amanda Guimarães, Clarice Antezana e Mateus Mussi**.

Quero manter a participação de todos reconhecida. Antes de escolher uma licença aberta, ainda precisamos alinhar essa decisão entre os autores e revisar os materiais de terceiros utilizados no projeto.
