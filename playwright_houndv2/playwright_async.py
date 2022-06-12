import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        print(await page.title())
        await browser.close()

asyncio.run(main())

import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as pw:
        browser = await pw.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://oficinajudicialvirtual.pjud.cl/indexN.php")

        # LOGIN PAGE
        await page.locator("//div[@id='focus']/button[@onclick='accesoConsultaCausas();']").click()
        await page.screenshot(path="proof.png")
        await browser.close()

asyncio.run(main())