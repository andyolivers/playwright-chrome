from fastapi import FastAPI
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get("/scrape")
def scrape_website(url: str = "https://www.python.org/"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        try:
            print("Opening page...")
            page.goto(url, timeout=10000)  # 10 seconds timeout
            content = page.content()
        except TimeoutError:
            content = "Timeout occurred while loading the page"
        finally:
            browser.close()

        return {"content": content}
