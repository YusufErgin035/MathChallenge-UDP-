import socket

# ip girilmez ise localhostta çalışır
class UDPComm:
    def __init__(self, buffer_size=1024):
        # UDP soketi oluşturuluyor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Alınacak veri boyutu sınırı
        self.buffer_size = buffer_size
        self.sock.bind("0.0.0.0",12345)
    def connect(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print("Eşleşme bekleniyor.")
            if addr is not None:
                print("Eşleşme başarılı.")
                self.sock.sendto(b"Mesaj alindi", addr)




    def send(self, data, addr=None):
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

