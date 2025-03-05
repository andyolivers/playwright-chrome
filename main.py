from fastapi import FastAPI
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import asyncio

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

@app.get("/scrape-async")
async def scrape_website_async(url: str = "https://www.python.org/"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await context.new_page()

        try:
            print("Opening page asynchronously...")
            await page.goto(url, timeout=10000)  # 10 seconds timeout
            content = await page.content()
        except TimeoutError:
            content = "Timeout occurred while loading the page"
        finally:
            await browser.close()

        return {"content": content}
