# Simulador Financeiro em Python 📊

Desenvolvi este projeto em equipe para colocar em prática meus estudos de **Python, desenvolvimento web, análise de dados e integração com APIs**.

A aplicação reúne um simulador de investimentos, gráficos interativos e ferramentas simples de organização financeira em uma interface web.

## 💡 Funcionalidades

| Módulo | Descrição |
|---|---|
| **Investimentos** | Simulação de aplicações com capital inicial, aportes mensais e gráficos de evolução |
| **Controle de gastos** | Registro de receitas e despesas por categorias |
| **Monitoramento** | Resumo financeiro com os valores informados |
| **Holerite** | Geração de uma planilha Excel ilustrativa |

O painel de investimentos utiliza indicadores como **SELIC, CDI e IPCA** e permite explorar a evolução histórica do **Bitcoin**.

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-008DE4?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)

Também utilizei **HTML, CSS, openpyxl, python-bcb e yfinance**.

## 📸 Conheça a interface

![Página inicial do Simulador Financeiro](docs/pagina-inicial.png)

Além da página inicial, o sistema possui telas de investimentos, holerite, gastos e monitoramento.

[Ver as cinco telas em execução no navegador](https://github.com/mateus-mussi/simulador-financeiro-python/actions/runs/44014061702)

## ▶️ Como executar

Para rodar o projeto, utilize **Python 3.11** e instale as dependências do repositório.

**1. Clone o projeto e crie um ambiente virtual:**

```bash
git clone https://github.com/mateus-mussi/simulador-financeiro-python.git
cd simulador-financeiro-python
python -m venv .venv
```

**2. Ative o ambiente virtual:**

No Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

**3. Instale as bibliotecas e inicie a aplicação:**

```bash
python -m pip install -r requirements.txt
python scripts/criar_holerite_modelo.py
python app.py
```

Acesse **http://127.0.0.1:5000** para abrir a página inicial ou **http://127.0.0.1:5000/dash/** para entrar diretamente no simulador.

## 🧪 Testes

Incluí testes automatizados para acompanhar o funcionamento das rotas web, dos cálculos, do controle de gastos e da geração de planilhas.

Para executá-los:

```bash
python -m unittest discover -s tests -v
```

O projeto também utiliza **GitHub Actions**. Em uma das execuções, foram aprovados **15 testes automatizados**, e as cinco páginas principais foram abertas em um navegador Chromium.

[Ver os resultados dos testes](https://github.com/mateus-mussi/simulador-financeiro-python/actions/runs/44013703245)

## 📈 Sobre os cálculos

O simulador considera aportes mensais e permite visualizar a evolução do saldo por dia, mês ou ano. Para as simulações de renda fixa, utiliza séries diárias de SELIC e CDI; o IPCA é usado para estimar o valor do saldo final ajustado pela inflação.

As simulações são **educativas**. O cenário de CDB é hipotético, e os valores apresentados não incluem todas as condições de investimentos reais, como impostos e tarifas. Os testes automatizados dos cálculos usam dados controlados, enquanto as consultas financeiras dependem de fontes externas.

## 👥 Desenvolvimento

Desenvolvi este projeto em grupo com **Amanda Guimarães** e **Clarice Antezana**.

Mantenho o repositório como parte do meu portfólio e da minha experiência com aplicações web em Python.
