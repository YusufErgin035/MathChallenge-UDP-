from udp_module import UDPConnection
import socket
import json
import random

# data:
#   - status: -1 => error, 0 => send, 1 => okey
#   - func: 0 => Are you active? 1 => game request client to server
#   - msg: -
#   - msg_id: int
#   - answer_id: int
class Core:
    def __init__(self):
        self.is_active = False
        self.target_port=12345
        self.is_connect = False
        self.conn = UDPConnection(on_message=self.handle_incoming, local_ip="0.0.0.0", local_port=12345)

    def set_target(self, target_ip, target_port=12345, target_name=""):
        self.target_ip = target_ip
        self.target_port = target_port
        self.target_name = target_name
        self.is_connect = True

    def handle_incoming(self, message, addr):
        if not self.is_connect:
            self.set_target(addr[0], 12345, "")
            
        try: # json çözümleme
            data = json.loads(message)
            status_value = data.get("status", None)
            func_value = data.get("func", None)
            msg_id_value = data.get("msg_id", 0)
            msg_value = data.get("msg", {})
            
            if status_value == 0 and func_value == 0:
                return_data = {"status": 1, "func": 0, "answer_id": msg_id_value}
                self.conn.send(self.target_ip, self.target_port, json.dumps(return_data))
            elif status_value == 1 and func_value == 0:
                self.is_active = True
            elif status_value == 1 and func_value == 1:
                self.is_game_request = True
            else:
                print(f"[{addr[0]}:{addr[1]}]: {data}")
        except: # json değilse
            print(f"[{addr[0]}:{addr[1]}]: {message}")
    
    def safe_random(self):
        return random.randint(10000, 99999)
    
    def send_areuactive(self, target_ip):
        return_data = {"status": 0, "func": 0, "msg_id": self.safe_random()}
        self.conn.send(target_ip, self.target_port, json.dumps(return_data))

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

    # msg
    #   my_ip
    #   my_port
    #   my_name
    def send_game_request(self):
        return_data = {"status": 0, "func": 1, "msg_id": self.safe_random(), "msg": {"my_ip": self.my_ip, "my_port": self.my_port, "my_name": self.my_name}}
        self.conn.send(self.target_ip, self.target_port, json.dumps(return_data))

    def stop(self):
        self.conn.stop()