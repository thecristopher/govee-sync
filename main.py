import sys
import json
from discover import discover_devices
from device import turn_on, turn_off, set_color
from audio_sync import start_audio_sync
from sync_screen import start_screen_sync

def load_devices():
    try:
        with open("devices.json", "r") as f:
            devices = json.load(f)
            print(f"📁 {len(devices)} dispositivos cargados desde devices.json")
            return devices
    except Exception as e:
        print("📂 No se pudo cargar devices.json:", e)
        return []

def print_help():
    print("Uso:")
    print("  python main.py discover           # Detecta y guarda todos los dispositivos")
    print("  python main.py on")
    print("  python main.py off")
    print("  python main.py color R G B")
    print("  python main.py sync-audio")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "discover":
        print("📡 Escaneando la red en busca de luces Govee...")
        devices = discover_devices()
        if not devices:
            print("❌ No se encontraron dispositivos.")
            sys.exit(0)

        for i, dev in enumerate(devices, 1):
            print(f" {i}) IP: {dev['ip']}, MAC: {dev['mac']}, Modelo: {dev.get('sku', 'Desconocido')}")

        # Agregar alias opcional
        for i, dev in enumerate(devices):
            nombre_sugerido = dev.get("sku", "Dispositivo") + f"_{i+1}"
            alias = input(f"  ➤ Alias para {dev['sku']} ({dev['ip']}): [{nombre_sugerido}] ") or nombre_sugerido
            dev["alias"] = alias


        with open("devices.json", "w") as f:
            json.dump(devices, f, indent=2)
        print("✅ Dispositivos guardados en devices.json")
        sys.exit(0)

    print(f"🧠 Comando recibido: {command}")
    devices = load_devices()
    if not devices:
        print("❌ No hay dispositivos guardados. Usa `python main.py discover` primero.")
        sys.exit(1)

    if command == "on":
        print("🔌 Encendiendo todas las luces...")
        for d in devices:
            turn_on(d)
    elif command == "off":
        print("💤 Apagando todas las luces...")
        for d in devices:
            turn_off(d)
    elif command == "color":
        if len(sys.argv) != 5:
            print("❌ Debes proporcionar R G B (0–255)")
            sys.exit(1)
        r, g, b = map(int, sys.argv[2:5])
        print(f"🎨 Cambiando color a: R={r} G={g} B={b}")
        for d in devices:
            set_color(d, r, g, b)
    elif command == "sync-audio":
        start_audio_sync()
    elif command == "sync-screen":
        start_screen_sync()
    else:
        print_help()

