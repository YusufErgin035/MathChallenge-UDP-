from src.udp_module import UDPConnection
import socket
import json
import random

class Core:
    def __init__(self):
        self.is_active = False
        self.target_port = 12345
        self.is_connect = False
        self.is_game_request = False
        self.is_game_accepted = False
        self.is_game_started = False
        self.on_game_request_callback = None  # 🔧 GUI callback
        self.conn = UDPConnection(on_message=self.handle_incoming, local_ip="0.0.0.0", local_port=12345)
        self.conn.start()

    def set_target(self, target_ip, target_port=12345, target_name=""):
        self.target_ip = target_ip
        self.target_port = target_port
        self.target_name = target_name
        self.is_connect = True

    def handle_incoming(self, message, addr):
        print(addr, message)
        if not self.is_connect:
            self.set_target(addr[0], 12345, "")

        try:
            data = json.loads(message)
            status_value = data.get("status", None)
            func_value = data.get("func", None)
            msg_id_value = data.get("msg_id", 0)

            if status_value == 0 and func_value == 0:
                print("00 - handle")
                return_data = {"status": 1, "func": 0, "answer_id": msg_id_value}
                self.conn.send(self.target_ip, self.target_port, json.dumps(return_data))

            elif status_value == 1 and func_value == 0:
                print("10 - handle")
                self.is_active = True

            elif status_value == 0 and func_value == 1:
                print("01 - handle")
                return_data = {"status": 1, "func": 1, "answer_id": msg_id_value}
                self.conn.send(self.target_ip, self.target_port, json.dumps(return_data))
                self.is_game_request = True

                if self.on_game_request_callback:
                    self.on_game_request_callback()

            elif status_value == 1 and func_value == 1:
                print("11 - handle")
                self.is_game_request = True

            elif status_value == 0 and func_value == 2:
                print("02 - handle")
                self.is_game_accepted = True
            elif status_value == 0 and func_value == 3:
                print("03 - handle")
                self.is_game_started = True
                msg = data.get("msg", {})
                is_answer = msg.get("isAnswer")
                question = msg.get("question")
                answer = msg.get("answer")
                print("Veri alındı:", is_answer, question, answer)
                if self.on_game_data_callback:
                    self.on_game_data_callback(is_answer, question, answer)
            else:
                print(f"[{addr[0]}:{addr[1]}]: {data}")
        except:
            print(f"[{addr[0]}:{addr[1]}]: {message}")

    def safe_random(self):
        return random.randint(10000, 99999)

    def send_areuactive(self, target_ip):
        return_data = {"status": 0, "func": 0, "msg_id": self.safe_random()}
        self.conn.send(target_ip, self.target_port, json.dumps(return_data))

    def send_game_request(self):
        return_data = {"status": 0, "func": 1, "msg_id": self.safe_random()}
        self.conn.send(self.target_ip, self.target_port, json.dumps(return_data))

    def send_accept_game_request(self):
        return_data = {"status": 0, "func": 2, "msg_id": self.safe_random()}
        self.conn.send(self.target_ip, self.target_port, json.dumps(return_data))

    def send_game_start(self):
        return_data = {"status": 0, "func": 3, "msg_id": self.safe_random()}
        self.conn.send(self.target_ip, self.target_port, json.dumps(return_data))

    def send_msg(self, msg):
        self.conn.send(self.target_ip, self.target_port, msg)

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP

    def stop(self):
        self.conn.stop()
