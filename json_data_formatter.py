import json

def transform_gsmarena_to_formatted(data):
    new_data = {}

    # --- Camera ---
    cam = data["specs"].get("MAIN CAMERA", {})
    selfie = data["specs"].get("SELFIE CAMERA", {})
    new_data["Camera"] = {
        "Main camera:": cam.get("Single") or cam.get("Triple") or cam.get("Dual") or "",
        "Flash:": cam.get("Features", ""),
        "Front:": selfie.get("Single", ""),
        "Video recording:": cam.get("Video", ""),
    }

    # --- Design ---
    body = data["specs"].get("BODY", {})
    new_data["Design"] = {
        "Dimensions:": body.get("Dimensions", ""),
        "Weight:": body.get("Weight", ""),
        "Colors:": data["specs"].get("MISC", {}).get("Colors", ""),
        "Materials:": "",  # GSMArena দেয় না, চাইলে ম্যানুয়ালি map করা যাবে
        "Biometrics:": "",  # Example placeholder
        "Resistance:": "",  # Example placeholder
    }

    # --- Battery ---
    battery = data["specs"].get("BATTERY", {})
    new_data["Battery"] = {
        "Type:": battery.get("Type", ""),
        "Capacity:": battery.get("Type", "").split()[1] if "mAh" in battery.get("Type", "") else "",
        "Charging:": battery.get("Charging", ""),
    }

    # --- Display ---
    display = data["specs"].get("DISPLAY", {})
    new_data["Display"] = {
        "Size:": display.get("Size", ""),
        "Resolution:": display.get("Resolution", ""),
        "Technology:": display.get("Type", ""),
        "Refresh rate:": display.get("", ""),  # কিছু সময় Hz আলাদা ফিল্ডে থাকে
    }

    # --- Cellular ---
    network = data["specs"].get("NETWORK", {})
    new_data["Cellular"] = {
        "5G:": network.get("Technology", ""),
        "SIM type:": body.get("SIM", ""),
    }

    # --- Hardware ---
    platform = data["specs"].get("PLATFORM", {})
    memory = data["specs"].get("MEMORY", {})
    new_data["Hardware"] = {
        "OS:": platform.get("OS", ""),
        "Processor:": platform.get("CPU", ""),
        "Internal storage:": memory.get("Internal", ""),
        "RAM:": memory.get("Internal", "").split()[-2] if "RAM" in memory.get("Internal", "") else "",
        "Device type:": "",  # Example placeholder
    }

    # --- Multimedia ---
    sound = data["specs"].get("SOUND", {})
    new_data["Multimedia"] = {
        "Speakers:": sound.get("Loudspeaker", ""),
        "Headphones:": sound.get("3.5mm jack", ""),
    }

    # --- Connectivity & Features ---
    comms = data["specs"].get("COMMS", {})
    features = data["specs"].get("FEATURES", {})
    new_data["Connectivity & Features"] = {
        "USB:": comms.get("USB", ""),
        "Wi-Fi:": comms.get("WLAN", ""),
        "Bluetooth:": comms.get("Bluetooth", ""),
        "Location:": comms.get("Positioning", ""),
        "Other:": "NFC: " + comms.get("NFC", "No"),
        "Sensors:": features.get("Sensors", ""),
    }

    return new_data


if __name__ == "__main__":
    # GSMArena scraped JSON file load করো
    with open("Huawei_MatePad_12_X_(2025)_20250919-211739.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    formatted = transform_gsmarena_to_formatted(raw_data)

    with open("formatted_device.json", "w", encoding="utf-8") as f:
        json.dump(formatted, f, ensure_ascii=False, indent=2)

    print("✅ Transformed JSON saved as formatted_device.json")
