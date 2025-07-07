import socket
import json

def send_udp(device, payload):
    print(f"📤 Enviando a {device['ip']}:4003 → {json.dumps(payload)}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(payload).encode(), (device["ip"], 4003))
    sock.close()

def turn_on(device):
    send_udp(device, {
        "msg": {
            "cmd": "turn",
            "data": {"value": 1}
        }
    })

def turn_off(device):
    send_udp(device, {
        "msg": {
            "cmd": "turn",
            "data": {"value": 0}
        }
    })

def set_color(device, r, g, b):
    send_udp(device, {
        "msg": {
            "cmd": "colorwc",
            "data": {"r": r, "g": g, "b": b}
        }
    })

