import sounddevice as sd
import numpy as np
import json
import time
from device import send_udp
import random
from concurrent.futures import ThreadPoolExecutor

# 🎨 Conversión HSV a RGB
def hsv_to_rgb(h, s, v):
    i = int(h * 6)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6

    if i == 0: return v, t, p
    if i == 1: return q, v, p
    if i == 2: return p, v, t
    if i == 3: return p, q, v
    if i == 4: return t, p, v
    if i == 5: return v, p, q

last_bounce = [0]
current_hue = [random.random()]  # estado global compartido

def volume_to_rgb(volume):
    amplified = min(1.0, volume * 100)
    brightness = max(0.25, amplified)

    now = time.time()
    bounce_interval = 0.2 + (1.0 - amplified) * 1.5  # cuanto más volumen, más rápido

    if now - last_bounce[0] > bounce_interval:
        new_hue = (current_hue[0] + random.uniform(0.3, 0.6)) % 1
        current_hue[0] = new_hue
        last_bounce[0] = now

    hue = current_hue[0]
    sat = 1.0

    # 💫 Si es volumen muy bajo, un modo más suave
    if volume < 0.003:
        brightness = 0.1
        sat = 0.7

    r, g, b = hsv_to_rgb(hue, sat, brightness)
    return {
        "color": {
            "r": int(r * 255),
            "g": int(g * 255),
            "b": int(b * 255)
        },
        "colorTemInKelvin": 0
    }

# 🚨 Enviar color como 'colorwc'
def set_color_udp(device, color_data):
    payload = {
        "msg": {
            "cmd": "colorwc",
            "data": color_data
        }
    }
    send_udp(device, payload)

executor = ThreadPoolExecutor(max_workers = 10)

# 🎧 Iniciar sincronización
def start_audio_sync():
    print("🎤 Iniciando sincronización por audio desde el sistema (modo visual)...")

    with open("devices.json", "r") as f:
        devices = json.load(f)

    preferred_name = "ckb-next music visualizer"
    all_devices = sd.query_devices()
    device_index = None

    for i, dev in enumerate(all_devices):
        if preferred_name.lower() in dev['name'].lower():
            device_index = i
            break

    if device_index is None:
        print(f"❌ No se encontró ningún dispositivo con '{preferred_name}'")
        return

    selected = all_devices[device_index]
    print(f"✅ Dispositivo seleccionado: {selected['name']} (index {device_index})")

    last_color = [None]  # mutable closure para comparar colores

    def audio_callback(indata, frames, time_info, status):
        try:
            volume_norm = np.linalg.norm(indata) / len(indata)
            color_data = volume_to_rgb(volume_norm)

            if color_data != last_color[0]:
                last_color[0] = color_data
                print(f"🔊 Volumen: {volume_norm:.3f} → Color: {color_data['color']}")
                for device in devices:
                    executor.submit(set_color_udp, device, color_data)
        except Exception as e:
            print(f"⚠️ Error en callback de audio: {e}")

    try:
        with sd.InputStream(device=device_index, channels=1, samplerate=48000, callback=audio_callback):
            print(f"📡 Escuchando desde: {selected['name']}")
            while True:
                time.sleep(0.1)
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e}")

