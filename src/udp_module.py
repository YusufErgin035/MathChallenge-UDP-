import socket
import threading

class UDPConnection:
    def __init__(self, on_message, local_ip="0.0.0.0", local_port=12345):
        self.local_ip = local_ip
        self.local_port = local_port
        self.on_message = on_message
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((local_ip, local_port))
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def listen_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                message = data.decode('utf-8')
                self.on_message(message, addr)
            except Exception as e:
                print(f"Error: {e}")

    def send(self, target_ip, target_port, message):
        self.sock.sendto(message.encode('utf-8'), (target_ip, target_port))

    def stop(self):
        self.running = False
        self.sock.close()
