"""Testes do módulo de dados financeiros, sem dependências externas."""
import unittest
import bd

class TestDadosFinanceiros(unittest.TestCase):
    def setUp(self):
        bd.salvar_no_bd({})

    def test_agrupa_receitas_e_despesas(self):
        bd.salvar_no_bd({"salario_jan": "3500.00", "energia_jan": "230.50", "iptu_jan": "120,00"})
        dados = bd.obter_dados()
        self.assertEqual(dados["RECEITAS"]["salario"], 3500.0)
        self.assertEqual(dados["DESPESAS FIXAS"]["energia"], 230.5)
        self.assertEqual(dados["DESPESAS FIXAS"]["iptu"], 120.0)

    def test_investimentos_nao_entram_como_despesas(self):
        bd.salvar_no_bd({"acoes_jan": "100", "salario_jan": "2000"})
        dados = bd.obter_dados()
        self.assertNotIn("acoes", dados["DESPESAS FIXAS"])
        self.assertEqual(dados["RECEITAS"]["salario"], 2000.0)

    def test_ignora_valores_invalidos(self):
        bd.salvar_no_bd({"salario_jan": "abc", "energia_jan": "17"})
        dados = bd.obter_dados()
        self.assertNotIn("salario", dados["RECEITAS"])
        self.assertEqual(dados["DESPESAS FIXAS"]["energia"], 17.0)

if __name__ == "__main__":
    unittest.main()
