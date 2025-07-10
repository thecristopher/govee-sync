import time
import json
from PIL import Image
from io import BytesIO
from collections import Counter
from device import send_udp
from pydbus import SessionBus
import base64

def capture_screen_via_dbus():
    bus = SessionBus()
    screenshot = bus.get("org.gnome.Shell.Screenshot")

    success, img_bytes = screenshot.Screenshot(False, False, "")  # False = sin flash
    if not success:
        raise RuntimeError("❌ No se pudo capturar la pantalla via DBus")

    data = base64.b64decode(img_bytes)
    return Image.open(BytesIO(data))

def get_dominant_color_from_image(img):
    img = img.resize((50, 50))
    pixels = list(img.getdata())
    color = Counter(pixels).most_common(1)[0][0]
    return color[:3]  # R, G, B

def start_screen_sync():
    print("🖥️ Iniciando sincronización con pantalla vía DBus...")

    try:
        with open("devices.json", "r") as f:
            devices = json.load(f)
    except Exception as e:
        print(f"❌ Error al cargar devices.json: {e}")
        return

    while True:
        try:
            img = capture_screen_via_dbus()
            r, g, b = get_dominant_color_from_image(img)
            print(f"🎨 Color dominante: R={r} G={g} B={b}")

            for device in devices:
                payload = {
                    "msg": {
                        "cmd": "colorwc",
                        "data": {"r": r, "g": g, "b": b}
                    }
                }
                send_udp(device, payload)

        except Exception as e:
            print(f"⚠️ Error capturando o procesando la pantalla: {e}")

        time.sleep(0.2)

