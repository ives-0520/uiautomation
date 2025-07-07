import asyncio
import re
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://gtt-account-web-lion.vdemosit.com/")
    await page.locator("iframe[title=\"Widget containing checkbox for hCaptcha security challenge\"]").content_frame.get_by_role("checkbox", name="This hCaptcha is for testing").click()
    await page.get_by_role("textbox", name="e-mail account").click()
    await page.get_by_role("textbox", name="e-mail account").fill("ives.he@gooseott.com")
    await page.get_by_role("button", name="Continue").click()
    await page.get_by_role("textbox", name="password").click()
    await page.get_by_role("textbox", name="password").fill("123456Aa")
    await page.get_by_role("button", name="Login").click()
    
    await page.get_by_role("menuitem", name="BASE SETUP").locator("span").click()
    await page.get_by_text("BRAND MANAGEMENT").click()
    await page.get_by_role("button", name="CREATE BRAND").click()

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
