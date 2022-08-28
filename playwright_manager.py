def run(playwright):
    # --- Initialize ---
    START_URL = "https://oficinajudicialvirtual.pjud.cl/indexN.php"

    # create browser instance
    firefox = playwright.firefox
    browser = firefox.launch(headless=True)

    # create isolated browser context
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )

    page = context.new_page()

    # --- Login Page ---
    response = page.goto(START_URL)
    # print(response.request.all_headers()) # Check if can pass headers from playwright to requests

    page.locator(
        "#focus button[onclick='accesoConsultaCausas();']",
        has_text="Consulta causas",
    ).click()

    # --- Fill Case Search Form ---
    page.select_option("select#competencia", label="Corte Apelaciones", force=True, value="2")  # Competencia
    page.select_option("select#conCorte", label="C.A. de La Serena", force=True, value="25")  # Corte

    page.type("input#conRolCausa", "3298", delay=100)  # ROL - TODO remove hardcode
    page.type("input#conEraCausa", "2022", delay=100)  # AÑO - TODO remove hardcode

    page.mouse.click(1000, 1000)

    # page.locator("select#conTipoCausa").click()
    page.select_option("select#conTipoCausa", label="Protección")  # Tipo

    page.locator("button#btnConConsulta").click()

    # page.locator("a[href='#modalDetalleApelaciones']").click()

    # --- Get Case Unique ID (JWT encoded data) ---
    original_jwt = page.locator("a[href='#modalDetalleApelaciones']").get_attribute("onclick")

    # --- Proof of Work ---
    # page.wait_for_timeout(3000)
    # page.screenshot(path="proof.png")
    # page.wait_for_timeout(30000000)

    browser.close()
    return original_jwt