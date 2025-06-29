from playwright.sync_api import sync_playwright
from colorama import Fore, Style


class BuscadorWeb:
    """Maneja las búsquedas web de forma separada"""

    @classmethod
    def buscar(cls, query: str) -> str:
        """Realiza una búsqueda web usando Playwright (Web scrapping)"""
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False, slow_mo=50)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113 Safari/537.36"
            )
            page = context.new_page()
            try:
                page.goto("https://duckduckgo.com")
                page.fill("input[name='q']", query)
                page.press("input[name='q']", "Enter")
                page.wait_for_selector("a.result__a", timeout=5000)
                result = page.inner_text("body").strip()
                return result
            except Exception as e:
                print(
                    f"{Fore.RED}{Style.BRIGHT}❌ Error en búsqueda web: {e}{Style.RESET_ALL}"
                )
                return "No se pudo obtener información de la web."
            finally:
                browser.close()
