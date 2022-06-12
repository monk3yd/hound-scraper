from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    # Use playwright.chromium, playwright.firefox or playwright.webkit
    # Pass headless=False to launch() to see the browser UI
    browser = pw.firefox.launch()
    page = browser.new_page()
    page.goto("https://google.com")
    page.screenshot(path="proof.png")
    browser.close()
