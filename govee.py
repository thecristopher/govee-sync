import requests
import json

def load_devices():
    with open("devices.json", "r") as f:
        return json.load(f)

def set_brightness_all(brightness):
    devices = load_devices()
    for device in devices:
        ip = device["ip"]
        payload = {
            "command": "brightness",
            "parameter": brightness
        }
        try:
            response = requests.put(f"http://{ip}/devices/control", json=payload)
            print(f"💡 {device['alias']} → Brillo {brightness}%")
        except Exception as e:
            print(f"❌ Error con {device['alias']}: {e}")

