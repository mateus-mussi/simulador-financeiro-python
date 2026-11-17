"""Gera um modelo fictício de holerite para demonstrar o projeto.
Execute na raiz: python scripts/criar_holerite_modelo.py
Não produz documentos trabalhistas oficiais.
"""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

DESTINO = Path(__file__).resolve().parents[1] / "holerite_modelo.xlsx"

def criar_modelo(destino=DESTINO):
    destino = Path(destino)
    if destino.exists():
        print(f"Arquivo preservado (já existe): {destino}")
        return False
    wb = Workbook()
    ws = wb.active
    ws.title = "contracheque"
    etiquetas = {
        "B2": "CONTRACHEQUE – MODELO DIDÁTICO",
        "B3": "Empresa:", "B5": "CNPJ:", "F5": "Competência:",
        "B7": "Cargo:", "B8": "Matrícula:", "C9": "Colaborador:",
        "B10": "Admissão:", "D14": "Proventos / benefícios",
        "G14": "Salário base:", "J14": "Descontos",
        "B36": "Documento ilustrativo. Sem validade fiscal ou trabalhista.",
    }
    for endereco, rotulo in etiquetas.items():
        ws[endereco] = rotulo
    for coluna, largura in {"B": 20, "C": 18, "D": 30, "G": 22, "H": 20, "K": 16}.items():
        ws.column_dimensions[coluna].width = largura
    for addr in ("B2", "D14", "G14", "J14"):
        ws[addr].font = Font(bold=True, color="FFFFFF")
        ws[addr].fill = PatternFill(fill_type="solid", fgColor="244369")
    ws["B36"].font = Font(italic=True, color="A00000")
    for linha in range(14, 36):
        ws[f"H{linha}"].number_format = '"R$" #,##0.00'
        ws[f"K{linha}"].number_format = '"R$" #,##0.00'
    wb.save(destino)
    print(f"Modelo demonstrativo criado: {destino}")
    return True

if __name__ == "__main__":
    criar_modelo()
