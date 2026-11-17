"""Regressão: aportes não podem depender da frequência do gráfico.

Utiliza taxas sintéticas, sem fazer chamadas às APIs financeiras.
"""
import ast
from pathlib import Path
import unittest

import pandas as pd


class FonteSimulada:
    @staticmethod
    def get(codigos, start, end):
        indice = pd.bdate_range(start, end)
        return pd.DataFrame(
            {"SELIC": [0.04] * len(indice), "CDI": [0.04] * len(indice)},
            index=indice,
        )


def carregar_funcao():
    origem = Path(__file__).resolve().parents[1] / "app.py"
    arvore = ast.parse(origem.read_text(encoding="utf-8"))
    funcao = next(
        n for n in arvore.body
        if isinstance(n, ast.FunctionDef) and n.name == "DadosInvestimento"
    )
    contexto = {"pd": pd, "sgs": FonteSimulada()}
    exec(
        compile(ast.Module(body=[funcao], type_ignores=[]), str(origem), "exec"),
        contexto,
    )
    return contexto["DadosInvestimento"]


class TestAportes(unittest.TestCase):
    def test_mesma_aplicacao_com_graficos_mensal_e_anual(self):
        calcular = carregar_funcao()
        capital = 1000.0
        inicio = pd.Timestamp("2025-01-01")
        fim = pd.Timestamp("2025-12-01")
        mensal = calcular(capital, inicio, fim, "M", "Baixo", 100.0)
        anual = calcular(capital, inicio, fim, "Y", "Baixo", 100.0)

        self.assertEqual(mensal[1], 2100.0)
        self.assertEqual(anual[1], 2100.0)
        self.assertAlmostEqual(mensal[2], anual[2])
        self.assertAlmostEqual(mensal[0].iloc[-1], anual[0].iloc[-1])


if __name__ == "__main__":
    unittest.main()
