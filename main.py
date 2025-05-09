import sys
import time
import random
from udp_modulu import UDPComm

# Giriş argümanı: 0 = ilk gönderen, 1 = ilk alıcı
if len(sys.argv) != 2 or sys.argv[1] not in ("0", "1"):
    print("Kullanim: python main.py [0|1]")
    sys.exit(1)

is_sender = sys.argv[1] == "0"

# Port ayarları
MY_PORT = 12345 if is_sender else 12346
PEER_PORT = 12346 if is_sender else 12345
IP = "127.0.0.1"

# UDP iletişim nesnesi başlat
udp = UDPComm(is_server=True, ip=IP, port=MY_PORT)

# Peer adresi (önceden bildiğimiz için sabit)
peer_addr = (IP, PEER_PORT)

# Gönder fonksiyonu
def send_random():
    num = random.randint(1, 100)
    print(f"[SEND] Sayı gönderiliyor: {num}")
    udp.send(f"SAYI:{num}", peer_addr)

# Alma fonksiyonu
def receive_number():
    msg, addr = udp.receive(timeout=5)
    if msg:
        print(f"[RECV] Gelen mesaj: {msg}")
        return True
    else:
        print("[RECV] Zaman aşımı, tekrar dene...")
        return False

# Eğer ilk gönderen isek başla
if is_sender:
    time.sleep(1)
    send_random()

# Sürekli sırayla al/gönder yap
while True:
    if receive_number():
        time.sleep(1)
        send_random()
