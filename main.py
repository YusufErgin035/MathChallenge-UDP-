import sys
import time
import random
from xml.etree.ElementTree import tostring

from udp_modulu import UDPComm
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Err: {e}"

print("Yerel IP Adresi:", get_local_ip())

IP = tostring(get_local_ip())

# UDP iletişim nesnesi başlat
udp = UDPComm( ip=IP, port=12345)

# Alma fonksiyonu
def receive_number():
    msg, addr = udp.receive(timeout=5)
    if msg:
        print(f"[RECV] Gelen mesaj: {msg}")
        return True
    else:
        print("[RECV] Zaman aşımı, tekrar dene...")
        return False
