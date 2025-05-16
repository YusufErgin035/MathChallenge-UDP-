from core import Core

def main():
    local_ip = "0.0.0.0"
    local_port = 12345
    target_ip = input("Target IP: ")
    target_port = 12345

    core = Core(target_ip)

    print("\nYou can start writing messages (type 'exit' to exit)(0 - send_areuactive)(1 - get_ip LOCAL):")
    while True:
        msg = input("> ")
        if msg.lower() == "exit":
            core.stop()
            break
        elif msg.lower() == "0":
            core.send_areuactive()    
        elif msg.lower() == "1":
            print(core.get_ip())
        else:
            core.send_msg(msg)

if __name__ == "__main__":
    main()