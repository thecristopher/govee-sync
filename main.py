from discover import discover_devices
from device import turn_on, turn_off, set_color

devices = discover_devices()

if not devices:
    print("❌ No se encontraron luces Govee.")
    exit()

# Solo probamos con la primera por ahora
light = devices[0]
print(f"🎯 Luz objetivo: {light['mac']} @ {light['ip']}")

turn_on(light)

