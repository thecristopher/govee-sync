import socket
import json
import time

MULTICAST_GROUP = "239.255.255.250"
SEND_PORT = 4001
RECEIVE_PORT = 4002
TIMEOUT = 5

def discover_devices():
    scan_message = {
        "msg": {
            "cmd": "scan",
            "data": {
                "account_topic": "reserve"
            }
        }
    }

    # Paso 1: Enviar mensaje a 239.255.255.250:4001
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    send_sock.sendto(json.dumps(scan_message).encode(), (MULTICAST_GROUP, SEND_PORT))
    send_sock.close()

    # Paso 2: Escuchar en 0.0.0.0:4002 por las respuestas
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_sock.bind(("", RECEIVE_PORT))
    recv_sock.settimeout(TIMEOUT)

    print("🔍 Escaneando luces Govee en la red...")
    devices = []
    start = time.time()

    try:
        while time.time() - start < TIMEOUT:
            data, addr = recv_sock.recvfrom(1024)
            print(f"📥 Paquete recibido de {addr}")
            try:
                response = json.loads(data)
                dev = response.get("msg", {}).get("data", {})
                if "ip" in dev and "device" in dev:
                    devices.append({
                        "ip": dev["ip"],
                        "mac": dev["device"],
                        "sku": dev.get("sku", "Desconocido")
                    })
                    print(f"✅ {dev['ip']} ({dev['device']}) modelo {dev.get('sku', '??')}")
            except Exception as e:
                print("⚠️ Error al parsear respuesta:", e)
    except socket.timeout:
        print("⏱️ Fin del escaneo")

    recv_sock.close()
    return devices

