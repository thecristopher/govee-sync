import socket
import json
import time

MULTICAST_GROUP = "239.255.255.250"
DISCOVERY_PORT_SEND = 4001
DISCOVERY_PORT_RECV = 4002
CONTROL_PORT = 4003

def discover_devices(timeout=5):
    # Mensaje oficial según docs de Govee
    scan_message = {
        "msg": {
            "cmd": "scan",
            "data": {
                "account_topic": "reserve"
            }
        }
    }

    # Enviar mensaje de descubrimiento (multicast a 4001)
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    send_sock.sendto(
        json.dumps(scan_message).encode(),
        (MULTICAST_GROUP, DISCOVERY_PORT_SEND)
    )
    send_sock.close()

    # Escuchar respuestas en 4002
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.bind(("", DISCOVERY_PORT_RECV))
    recv_sock.settimeout(timeout)

    print("🔍 Escaneando luces Govee en la red...")

    devices = []
    start = time.time()

    try:
        while time.time() - start < timeout:
            data, addr = recv_sock.recvfrom(1024)
            response = json.loads(data)
            dev = response.get("msg", {}).get("data", {})

            if "ip" in dev and "device" in dev:
                devices.append({
                    "ip": dev["ip"],
                    "mac": dev["device"],
                    "sku": dev.get("sku", "Unknown")
                })
                print(f"✅ Detectado: {dev['ip']} ({dev['device']})")
    except socket.timeout:
        print("⏱️ Fin del escaneo")

    recv_sock.close()
    return devices

