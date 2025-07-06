import asyncio
import os
from PIL import Image
from govee_api_laggat import Govee

API_KEY = "API_KEY"

# Nombres de dispositivos a sincronizar (puedes agregar más)
TARGET_DEVICE_NAMES = ["Dispositivo 1"]

SCREENSHOT_PATH = "/tmp/sync.png"

def get_avg_color_wayland():
    """Captura el escritorio y calcula el color promedio."""
    try:
        os.system(f"gnome-screenshot -f {SCREENSHOT_PATH}")
        with Image.open(SCREENSHOT_PATH) as img:
            img = img.resize((50, 50))
            pixels = list(img.getdata())
            r = sum(p[0] for p in pixels) // len(pixels)
            g = sum(p[1] for p in pixels) // len(pixels)
            b = sum(p[2] for p in pixels) // len(pixels)
            return (r, g, b)
    except Exception as e:
        print(f"❌ Error capturando imagen: {e}")
        return None

async def main():
    async with Govee(API_KEY) as govee:
        devices, _ = await govee.get_devices()

        if not devices:
            print("❌ No se detectaron dispositivos.")
            return

        target_devices = [
            d for d in devices
            if any(name.lower() in d.device_name.lower() for name in TARGET_DEVICE_NAMES)
        ]

        if not target_devices:
            print("❌ No se encontraron dispositivos con los nombres indicados.")
            return

        print("🎯 Controlando los siguientes dispositivos:")
        for d in target_devices:
            print(f" - {d.device_name} ({d.device})")

        last_color = None

        while True:
            color = get_avg_color_wayland()
            if not color or color == last_color:
                await asyncio.sleep(5)
                continue

            last_color = color
            for d in target_devices:
                try:
                    await govee.set_color(d.device, color)
                    print(f"🎨 {d.device_name}: Color actualizado a {color}")
                except Exception as e:
                    print(f"❌ {d.device_name}: Error al cambiar color: {e}")

            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())

