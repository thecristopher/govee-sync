import sys
import json
from discover import discover_devices
from device import turn_on, turn_off, set_color

def load_device():
    try:
        with open("settings.json", "r") as f:
            device = json.load(f)
            print(f"📁 Cargando dispositivo guardado: {device['ip']} ({device['mac']})")
            return device
    except Exception as e:
        print("📂 No se pudo cargar settings.json:", e)
        print("🔍 Escaneando luces Govee...")
        devices = discover_devices()
        if not devices:
            print("❌ No se encontraron luces.")
            sys.exit(1)

        device = devices[0]
        print(f"💾 Guardando dispositivo: {device['ip']} ({device['mac']})")
        with open("settings.json", "w") as f:
            json.dump(device, f, indent=2)
        return device

def print_help():
    print("Uso:")
    print("  python main.py discover          # Mostrar luces disponibles")
    print("  python main.py on")
    print("  python main.py off")
    print("  python main.py color R G B")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "discover":
        print("📡 Buscando dispositivos Govee...")
        devices = discover_devices()
        if not devices:
            print("❌ No se encontraron luces.")
            sys.exit(0)

        print("\n💡 Dispositivos detectados:")
        for i, d in enumerate(devices, 1):
            print(f" {i}) IP: {d['ip']}, MAC: {d['mac']}, Modelo: {d.get('sku', 'Desconocido')}")

        selection = input("\n🔘 ¿Deseas guardar uno como predeterminado? Ingresa el número (o presiona Enter para salir): ")
        if selection.isdigit():
            index = int(selection) - 1
            if 0 <= index < len(devices):
                with open("settings.json", "w") as f:
                    json.dump(devices[index], f, indent=2)
                print(f"💾 Guardado: {devices[index]['ip']} ({devices[index]['mac']})")
            else:
                print("❌ Selección inválida.")
        sys.exit(0)

    print(f"🧠 Comando recibido: {command}")
    device = load_device()

    if command == "on":
        print("🔌 Encendiendo luz...")
        turn_on(device)
    elif command == "off":
        print("💤 Apagando luz...")
        turn_off(device)
    elif command == "color":
        if len(sys.argv) != 5:
            print("❌ Debes proporcionar R G B (0–255)")
            sys.exit(1)
        r, g, b = map(int, sys.argv[2:5])
        print(f"🎨 Cambiando color a: R={r} G={g} B={b}")
        set_color(device, r, g, b)
    else:
        print_help()

