# Sistema de Gestão Financeira em Python

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-008DE4?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)

## Visão geral

Projeto acadêmico em equipe que reúne um **simulador de investimentos**, telas de gestão financeira e ferramentas didáticas para emissão de holerites. O objetivo é explorar desenvolvimento de interfaces web com Python, integração de fontes externas de dados e visualização interativa de indicadores financeiros.

**Desenvolvido em equipe por Amanda Guimarães, Clarice Antezana e Mateus Mussi**, conforme os créditos encontrados no material do projeto. O compartilhamento do código e a escolha de uma licença devem respeitar a autorização dos coautores.

## Funcionalidades previstas no projeto

| Módulo | Rota | Descrição |
|---|---|---|
| Página inicial | `/` | Apresentação e navegação entre funcionalidades |
| Simulador de investimentos | `/dash/` | Simulação e gráficos de aplicações com informações financeiras externas |
| Holerite | `/holerite` | Formulário e planilha ilustrativa |
| Gastos | `/gastos` | Cadastro e organização de receitas e despesas |
| Monitoramento | `/monitoramento` | Visão resumida dos dados financeiros |

## Tecnologias

- **Python e Flask:** servidor web e rotas;
- **Dash, Plotly e Dash Bootstrap Components:** gráficos e interface interativa;
- **Pandas:** processamento de séries e dados;
- **python-bcb:** consulta de indicadores do Banco Central;
- **yfinance:** consulta de informações de mercado;
- **openpyxl:** planilhas Excel;
- **HTML e CSS:** interface das páginas.

## Instalação e execução

**Pré-requisitos:** Python 3.11+, pip e conexão com a internet para as consultas às fontes externas.

```bash
git clone https://github.com/mateus-mussi/simulador-financeiro-python.git
cd simulador-financeiro-python
python -m venv .venv
```

Ative o ambiente no Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Ou no Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências e inicie a aplicação:

```bash
python -m pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000` e acesse o painel de investimentos em `http://127.0.0.1:5000/dash/`.

> **Status do desenvolvimento:** o projeto foi revisado parcialmente, mas ainda não passou por teste integral de execução. A simulação de investimentos requer validação das unidades das taxas (SELIC/CDI), periodicidade dos aportes e integração com as APIs, antes de ser utilizada para decisões reais.

## Demonstração visual

As capturas devem mostrar a aplicação efetivamente executada. O pacote de preparação inclui uma captura estática da página inicial, que **não comprova o funcionamento das integrações financeiras**. Imagens definitivas serão adicionadas à pasta `docs/` após validação.

## Estrutura do projeto

```text
simulador-financeiro-python/
├── app.py
├── bd.py
├── requirements.txt
├── templates/
├── static/
├── docs/
├── .gitignore
└── README.md
```

## Limitações conhecidas

- O módulo de gastos é um protótipo sem armazenamento persistente;
- A geração de holerites é ilustrativa e não tem validade trabalhista;
- Fórmulas financeiras, cotação de Bitcoin e tratamento de dados externos exigem revisão e testes;
- O código não deve receber dados pessoais ou financeiros reais sem medidas adicionais de segurança;
- Imagens pessoais, planilhas reais e credenciais não devem ser publicadas.

## Autoria e licença

O projeto é acadêmico e foi desenvolvido em grupo. **Nenhuma licença aberta foi aplicada automaticamente.** A inclusão do arquivo `LICENSE` depende da concordância dos coautores e da revisão de direitos sobre recursos externos.
