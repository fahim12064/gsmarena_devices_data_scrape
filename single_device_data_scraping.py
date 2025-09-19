from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def scrape_device(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Device name
        device_name = page.locator("h1.specs-phone-name-title").inner_text().strip()
        print(f"📱 Scraping: {device_name}")

        data = {"url": url}
        data["name"] = device_name

        # Image
        try:
            data["image"] = page.locator(".specs-photo-main img").get_attribute("src")
        except:
            data["image"] = None

        # Highlights
        highlights = page.locator(".specs-spotlight-features li")
        data["highlights"] = []
        for i in range(highlights.count()):
            data["highlights"].append(highlights.nth(i).inner_text().strip())

        # Full specs
        specs = {}
        tables = page.locator("#specs-list table")
        for t in range(tables.count()):
            rows = tables.nth(t).locator("tr")
            category = None
            for r in range(rows.count()):
                row = rows.nth(r)
                th = row.locator("th")
                if th.count() > 0:
                    category = th.inner_text().strip()
                    if category not in specs:
                        specs[category] = {}
                ttl = row.locator("td.ttl")
                nfo = row.locator("td.nfo")
                if ttl.count() > 0 and nfo.count() > 0:
                    key = ttl.inner_text().strip()
                    val = nfo.inner_text().strip()
                    specs[category][key] = val
        data["specs"] = specs

        browser.close()
        return data


def save_device_data(url):
    data = scrape_device(url)

    # filename safe name
    safe_name = data["name"].replace(" ", "_").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{safe_name}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved: {filename}")


if __name__ == "__main__":
    # Example link
    url = input("Please input the device link: ")
    save_device_data(url)
