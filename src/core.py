from udp_module import UDPConnection
import json
import random

# data:
#   - status: -1 => error, 0 => send, 1 => okey
#   - func: 0 => Are you active?
#   - msg: -
#   - msg_id: int
#   - answer_id: int
class Core:
    def __init__(self, target_ip, target_port=12345):
        self.target_ip = target_ip
        self.target_port=target_port

        self.conn = UDPConnection(on_message=self.handle_incoming, local_ip="0.0.0.0", local_port=12345)
        self.conn.start()

    def handle_incoming(self, message, addr):
        try: # json çözümleme
            data = json.loads(message)
            status_value = data.get("status", None)
            func_value = data.get("func", None)
            msg_id_value = data.get("msg_id", 0)
            
            if status_value == 0 and func_value == 0:
                return_data = {"status": 1, "func": 0, "answer_id": msg_id_value}
                self.conn.send(self.target_ip, self.target_port, json.dumps(return_data))
            elif status_value == 1 and func_value == 0:
                print(f"[{addr[0]}:{addr[1]}]: is ACTIVE!")
            else:
                print(f"[{addr[0]}:{addr[1]}]: {data}")
        except: # json değilse
            print(f"[{addr[0]}:{addr[1]}]: {message}")
    
    def safe_random(self):
        return random.randint(10000, 99999)
    
    def send_areuactive(self):
        return_data = {"status": 0, "func": 0, "msg_id": self.safe_random()}
        self.conn.send(self.target_ip, self.target_port, json.dumps(return_data))

    def send_msg(self, msg):
        self.conn.send(self.target_ip, self.target_port, msg)

    def stop(self):
        self.conn.stop()