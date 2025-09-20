from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime


# ---------- Utility: ensure folder ----------
def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


# ---------- Scraper ----------
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


# ---------- Formatter ----------
def transform_gsmarena_to_formatted(data):
    new_data = {}

    # Camera
    cam = data["specs"].get("MAIN CAMERA", {})
    selfie = data["specs"].get("SELFIE CAMERA", {})
    new_data["Camera"] = {
        "Main camera:": cam.get("Single") or cam.get("Triple") or cam.get("Dual") or "",
        "Flash:": cam.get("Features", ""),
        "Front:": selfie.get("Single", ""),
        "Video recording:": cam.get("Video", ""),
    }

    # Design
    body = data["specs"].get("BODY", {})
    new_data["Design"] = {
        "Dimensions:": body.get("Dimensions", ""),
        "Weight:": body.get("Weight", ""),
        "Colors:": data["specs"].get("MISC", {}).get("Colors", ""),
    }

    # Battery
    battery = data["specs"].get("BATTERY", {})
    new_data["Battery"] = {
        "Type:": battery.get("Type", ""),
        "Charging:": battery.get("Charging", ""),
    }

    # Display
    display = data["specs"].get("DISPLAY", {})
    new_data["Display"] = {
        "Size:": display.get("Size", ""),
        "Resolution:": display.get("Resolution", ""),
        "Technology:": display.get("Type", ""),
    }

    # Cellular
    network = data["specs"].get("NETWORK", {})
    new_data["Cellular"] = {
        "5G:": network.get("Technology", ""),
        "SIM type:": body.get("SIM", ""),
    }

    # Hardware
    platform = data["specs"].get("PLATFORM", {})
    memory = data["specs"].get("MEMORY", {})
    new_data["Hardware"] = {
        "OS:": platform.get("OS", ""),
        "Processor:": platform.get("CPU", ""),
        "Internal storage:": memory.get("Internal", ""),
    }

    # Multimedia
    sound = data["specs"].get("SOUND", {})
    new_data["Multimedia"] = {
        "Speakers:": sound.get("Loudspeaker", ""),
        "Headphones:": sound.get("3.5mm jack", ""),
    }

    # Connectivity & Features
    comms = data["specs"].get("COMMS", {})
    features = data["specs"].get("FEATURES", {})
    new_data["Connectivity & Features"] = {
        "USB:": comms.get("USB", ""),
        "Wi-Fi:": comms.get("WLAN", ""),
        "Bluetooth:": comms.get("Bluetooth", ""),
        "Location:": comms.get("Positioning", ""),
        "Sensors:": features.get("Sensors", ""),
    }

    return new_data


# ---------- Save Function ----------
def save_device_data(url):
    data = scrape_device(url)

    # Prepare filename
    safe_name = data["name"].replace(" ", "_").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Ensure folders
    ensure_folder("raw_data")
    ensure_folder("formatted_data")

    # Save raw JSON
    raw_filename = os.path.join("raw_data", f"{safe_name}_{timestamp}.json")
    with open(raw_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Raw data saved: {raw_filename}")

    # Transform + Save formatted JSON
    formatted = transform_gsmarena_to_formatted(data)
    formatted_filename = os.path.join("formatted_data", f"{safe_name}_{timestamp}.json")
    with open(formatted_filename, "w", encoding="utf-8") as f:
        json.dump(formatted, f, ensure_ascii=False, indent=2)
    print(f"✅ Formatted data saved: {formatted_filename}")


# ---------- Main ----------
if __name__ == "__main__":
    url = input("Please input the device link: ")
    save_device_data(url)
