import requests
import pandas as pd

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from jwt_manager import JWTManager
from playwright_manager import run


def main():
    # --- TODO - LOAD DATABASE FROM GDRIVE ---

    # --- PLAYWRIGHT ---
    with sync_playwright() as playwright:
        original_jwt = run(playwright)

    # This changes, need to get from playwright TODO
    # original_jwt = "detalleCausaApelaciones('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvb2ZpY2luYWp1ZGljaWFsdmlydHVhbC5wanVkLmNsIiwiYXVkIjoiaHR0cHM6XC9cL29maWNpbmFqdWRpY2lhbHZpcnR1YWwucGp1ZC5jbCIsImlhdCI6MTY2MTY3MzUxNCwiZXhwIjoxNjYxNjc1MzE0LCJkYXRhIjp7InJvbENhdXNhIjoiMzI5OCIsImVyYUNhdXNhIjoiMjAyMiIsImNvZENvcnRlIjoiMjUiLCJjb2RMaWJybyI6IjM0IiwiY29tb2RpbiI6MCwiZmxnX2Fub25pbWl6YWNpb24iOiIwIn19.iEJk5GsE4jH-hCmOS9oW_t3fHcHYsTT4zB3Ev1Ttn-c');"

    jwt_manager = JWTManager(original_jwt)
    jwt_manager.modify_to("1246", "2019")
    html = jwt_manager.request()

    soup = BeautifulSoup(html, "html.parser")
    df = pd.read_html(soup.prettify())
    # df.to_csv()


if __name__ == "__main__":
    main()
