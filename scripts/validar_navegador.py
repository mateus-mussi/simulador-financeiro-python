"""Captura e verifica páginas reais em navegador Chromium.
Uso: python scripts/validar_navegador.py
Requer app Flask em http://127.0.0.1:5000 e Playwright com Chromium.
Não executa cálculos externos no painel.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:5000"
OUTPUT = Path("artifacts/capturas")
OUTPUT.mkdir(parents=True, exist_ok=True)

PAGES = [
    ("inicio", "/"),
    ("investimentos", "/dash/"),
    ("holerite", "/holerite"),
    ("gastos", "/gastos"),
    ("monitoramento", "/monitoramento"),
]

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    for name, path in PAGES:
        response = page.goto(BASE_URL + path, wait_until="domcontentloaded", timeout=60000)
        if response is None or response.status != 200:
            raise RuntimeError(f"{path}: resposta HTTP inesperada: {response.status if response else 'sem resposta'}")
        if path == "/dash/":
            # O Dash renderiza a interface client-side após receber o HTML.
            page.locator("#CapitalInicial").wait_for(state="visible", timeout=45000)
            page.locator("#CalcularButton").wait_for(state="visible", timeout=45000)
        else:
            page.locator("body").wait_for(state="visible")
        destino = OUTPUT / (name + ".png")
        page.screenshot(path=str(destino), full_page=True)
        print(f"OK: {path} -> {destino}")
    browser.close()
