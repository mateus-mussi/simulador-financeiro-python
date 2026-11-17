"""Smoke tests da aplicação Flask + Dash usando bibliotecas reais, mas APIs simuladas.

Executar: python scripts/criar_holerite_modelo.py
          python -m unittest discover -s tests -v
"""
import unittest
from io import BytesIO
from unittest.mock import patch

import pandas as pd
from openpyxl import load_workbook

import app as projeto
import bd


class TestWeb(unittest.TestCase):
    def setUp(self):
        self.cliente = projeto.app.test_client()
        bd.salvar_no_bd({})

    def test_paginas_principais_abrem(self):
        for url in ["/", "/holerite", "/gastos", "/monitoramento", "/dash/"]:
            with self.subTest(url=url):
                resposta = self.cliente.get(url)
                self.assertEqual(
                    resposta.status_code, 200,
                    f"{url}: HTTP {resposta.status_code} - {resposta.data[:300]!r}"
                )

    def test_arquivos_estaticos(self):
        for url in ["/static/css/style.css", "/static/images/homepage.jpg"]:
            with self.subTest(url=url):
                self.assertEqual(self.cliente.get(url).status_code, 200)

    def test_receitas_e_monitoramento(self):
        resposta = self.cliente.post("/salvar_receitas", data={
            "salario_jan": "3500.00",
            "energia_jan": "200.00",
        }, follow_redirects=True)
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"Dashboard de Gastos", resposta.data)
        self.assertEqual(bd.obter_dados()["RECEITAS"]["salario"], 3500.0)

    def test_holerite_gera_planilha_didatica(self):
        resposta = self.cliente.post("/processar_holerite", data={
            "nome_empresa": "Empresa Exemplo",
            "cnpj_empresa": "00.000.000/0000-00",
            "data_holerite": "2026-01",
            "matricula": "EXEMPLO-001",
            "nome_funcionario": "Pessoa Fictícia",
            "salario": "2500",
            "cargo": "Cargo Didático",
            "admissao": "2025-01-01",
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            resposta.content_type,
        )
        wb = load_workbook(BytesIO(resposta.data), read_only=True)
        try:
            ws = wb["contracheque"]
            self.assertEqual(ws["C3"].value, "Empresa Exemplo")
            self.assertEqual(ws["D8"].value, "Pessoa Fictícia")
        finally:
            wb.close()

    def test_callback_dashboard_com_sgs_ficticio(self):
        def sgs_simulado(codigos, start, end):
            if "IPCA" in codigos:
                return pd.DataFrame(
                    {"IPCA": [0.5, 0.4]},
                    index=pd.to_datetime(["2025-01-01", "2025-02-01"]),
                )
            datas = pd.bdate_range(start, end)
            return pd.DataFrame(
                {"SELIC": [0.04] * len(datas), "CDI": [0.04] * len(datas)},
                index=datas,
            )

        with patch.object(projeto.sgs, "get", side_effect=sgs_simulado):
            figura, tabela, resumo = projeto.AtualizarGraficoETabela(
                1000, 100, "2025-01-01", "2025-03-01", "M", "Baixo", 1,
            )
        self.assertGreater(len(figura.data), 0)
        self.assertIsNotNone(tabela)
        self.assertIn("Total Investido", str(resumo))


if __name__ == "__main__":
    unittest.main()
