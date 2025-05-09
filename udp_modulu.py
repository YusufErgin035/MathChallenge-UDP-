import socket

# ip girilmez ise localhostta çalışır
class UDPComm:
    def __init__(self, is_server=False, ip="127.0.0.1", port=12345, buffer_size=1024):
        # UDP soketi oluşturuluyor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Alınacak veri boyutu sınırı
        self.buffer_size = buffer_size

        # Bu nesne sunucu mu, istemci mi?
        self.is_server = is_server

        if is_server:
            # Sunucuysa belirli bir IP ve port'a bind edilir (dinlemeye başlar)
            self.sock.bind((ip, port))
            print(f"[UDP Server] Dinleniyor: {ip}:{port}")
        else:
            # İstemciyse bağlanacağı sunucunun adresi saklanır
            self.server_addr = (ip, port)
            print(f"[UDP Client] Sunucuya hazir: {ip}:{port}")

    def send(self, data, addr=None):
        # Veri gönderme fonksiyonu
        # Sunucuysa hedef adresi belirtmek gerekir
        if self.is_server:
            if addr:
                # Sunucu, veriyi belirli bir istemci adresine gönderir
                self.sock.sendto(data.encode(), addr)
        else:
            # İstemci, veriyi önceden tanımlanmış sunucuya gönderir
            self.sock.sendto(data.encode(), self.server_addr)

    def receive(self, timeout=None):
        # Veri alma fonksiyonu, opsiyonel olarak timeout verilebilir
        if timeout:
            self.sock.settimeout(timeout)  # Belirli bir süre içinde cevap beklenir

        try:
            # Veri ve gönderen adres alınır
            data, addr = self.sock.recvfrom(self.buffer_size)
            return data.decode(), addr
        except socket.timeout:
            # Süre aşımı olursa None döner
            return None, None

    def close(self):
        # Bağlantıyı kapatır
        self.sock.close()
        print("[UDP] Baglanti kapatildi.")