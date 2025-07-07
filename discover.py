import socket
import json
import select
from colorama import Fore

MULTICAST_GROUP = "239.255.255.250"
PORT_SEND = 4001
PORT_RECV = 4002
TIMEOUT = 5

def discover_devices():
    print(Fore.YELLOW + "🔍 Escaneando luces Govee en la red...")

    # Socket para enviar
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Socket para recibir
    receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver.bind(("", PORT_RECV))
    receiver.settimeout(TIMEOUT)

    scan_message = {
        "msg": {
            "cmd": "scan",
            "data": {
                "account_topic": "reserve"
            }
        }
    }

    # Enviar mensaje scan a 239.255.255.250:4001
    sender.sendto(json.dumps(scan_message).encode(), (MULTICAST_GROUP, PORT_SEND))

    found_devices = []

    try:
        while True:
            ready = select.select([receiver], [], [], TIMEOUT)
            if ready[0]:
                data, addr = receiver.recvfrom(1024)
                print(Fore.CYAN + f"📥 Paquete recibido de {addr}")
                response = json.loads(data)

                if response.get("msg", {}).get("cmd") == "scan":
                    info = response["msg"]["data"]
                    device = {
                        "ip": info["ip"],
                        "mac": info["device"],
                        "sku": info.get("sku", "Desconocido")
                    }
                    if device not in found_devices:
                        found_devices.append(device)
                        print(Fore.GREEN + f"✅ {device['ip']} ({device['mac']}) modelo {device['sku']}")
            else:
                break
    except socket.timeout:
        pass
    finally:
        sender.close()
        receiver.close()

    print("⏱️ Fin del escaneo")
    return found_devices

