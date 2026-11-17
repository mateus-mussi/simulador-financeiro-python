"""Testes determinísticos das funções financeiras sem depender de API ou Flask."""
import ast
import unittest
from pathlib import Path

import pandas as pd


class FonteSGSFicticia:
    def __init__(self, taxa=0.04, ipca=None):
        self.taxa = taxa
        self.ipca = ipca

    def get(self, series, start, end):
        if "IPCA" in series:
            if self.ipca is not None:
                return self.ipca
            return pd.DataFrame(
                {"IPCA": [10.0, 10.0]},
                index=pd.to_datetime(["2025-01-01", "2025-02-01"]),
            )
        datas = pd.bdate_range(start, end)
        return pd.DataFrame(
            {"SELIC": [self.taxa] * len(datas), "CDI": [self.taxa] * len(datas)},
            index=datas,
        )


def carregar_funcao(nome, fonte):
    origem = Path(__file__).resolve().parents[1] / "app.py"
    arvore = ast.parse(origem.read_text(encoding="utf-8"))
    funcao = next(
        item
        for item in arvore.body
        if isinstance(item, ast.FunctionDef) and item.name == nome
    )
    contexto = {"pd": pd, "sgs": fonte}
    exec(compile(ast.Module(body=[funcao], type_ignores=[]), str(origem), "exec"), contexto)
    return contexto[nome]


class TestModeloFinanceiro(unittest.TestCase):
    def test_aportes_independentes_da_frequencia_do_grafico(self):
        calcular = carregar_funcao("DadosInvestimento", FonteSGSFicticia())
        parametros = (1000, "2025-01-01", "2025-12-01")
        mensal = calcular(*parametros, "M", "Baixo", 100)
        anual = calcular(*parametros, "Y", "Baixo", 100)
        self.assertEqual(mensal[1], 2100)
        self.assertEqual(anual[1], 2100)
        self.assertAlmostEqual(mensal[2], anual[2], places=5)
        self.assertAlmostEqual(mensal[0].iloc[-1], anual[0].iloc[-1], places=5)

    def test_sem_rendimento_somente_aportes(self):
        calcular = carregar_funcao("DadosInvestimento", FonteSGSFicticia(taxa=0))
        serie, investido, lucro = calcular(1000, "2025-01-01", "2025-04-01", "D", "Baixo", 100)
        self.assertEqual(investido, 1300)
        self.assertAlmostEqual(lucro, 0)
        self.assertAlmostEqual(serie.iloc[-1], 1300)

    def test_taxa_diaria_composta_em_dias_uteis(self):
        calcular = carregar_funcao("DadosInvestimento", FonteSGSFicticia(taxa=0.04))
        serie, investido, lucro = calcular(1000, "2025-01-01", "2025-01-08", "D", "Baixo", 0)
        self.assertAlmostEqual(serie.iloc[-1], 1000 * (1.0004 ** 5), places=6)
        self.assertAlmostEqual(lucro, serie.iloc[-1] - investido)

    def test_periodo_invalido(self):
        calcular = carregar_funcao("DadosInvestimento", FonteSGSFicticia())
        with self.assertRaises(ValueError):
            calcular(1000, "2025-03-02", "2025-01-01", "M", "Baixo", 100)

    def test_ipca_composto_e_capital_deflacionado(self):
        deflacionar = carregar_funcao("AjustarPorInflacao", FonteSGSFicticia())
        capital, inflacao = deflacionar(1210, "2025-01-01", "2025-02-28")
        self.assertAlmostEqual(inflacao, 21)
        self.assertAlmostEqual(capital, 1000)

    def test_ipca_sem_dados(self):
        deflacionar = carregar_funcao("AjustarPorInflacao", FonteSGSFicticia(ipca=pd.DataFrame()))
        with self.assertRaises(ValueError):
            deflacionar(1000, "2025-01-01", "2025-02-28")
