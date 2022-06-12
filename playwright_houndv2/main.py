from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def main():
    # TODO - Load database cases data
    with sync_playwright() as pw:
        # --- Browser init ---
        browser = pw.firefox.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )

        page = browser.new_page()
        page.goto("https://oficinajudicialvirtual.pjud.cl/indexN.php")

        # --- Login Page ---
        page.locator(
            "#focus button[onclick='accesoConsultaCausas();']",
            has_text="Consulta causas",
        ).click()

        # --- Fill Case Search Form ---
        page.select_option("select#competencia", label="Corte Apelaciones")
        page.select_option("select#conCorte", label="C.A. de La Serena")

        # TODO remove hardcode
        page.fill("input#conRolCausa", "3298")
        page.fill("input#conEraCausa", "2022")

        page.locator("select#conTipoCausa").click(force=True)
        page.select_option("select#conTipoCausa", label="Protección")

        page.locator("button#btnConConsulta").click()

        case_data = page.locator("a[href='#modalDetalleApelaciones']").click()

        page.wait_for_timeout(3000)

        html = page.content()

        soup = BeautifulSoup(html, "html.parser")
        print(soup.prettify())


        # --- Proof of Work ---
        page.wait_for_timeout(3000)
        page.screenshot(path="proof.png")
        browser.close()


if __name__ == "__main__":
    main()
