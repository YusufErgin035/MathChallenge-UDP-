from udp_module import UDPConnection

def main():
    local_ip = "0.0.0.0"
    local_port = 12345
    target_ip = input("Target IP: ")
    target_port = 12345

    def handle_incoming(message, addr):
        print(f"\n[{addr[0]}:{addr[1]}]: {message}")

    conn = UDPConnection(on_message=handle_incoming, local_ip=local_ip, local_port=local_port)
    conn.start()

    print("\nYou can start writing messages (type 'exit' to exit):")
    while True:
        msg = input("> ")
        if msg.lower() == "exit":
            conn.stop()
            break
        conn.send(target_ip, target_port, msg)

if __name__ == "__main__":
    main()
