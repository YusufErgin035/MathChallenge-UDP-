import customtkinter as ctk
import socket
import threading
import time
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MathHurdleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x1320")
        self.title("MathHurdle")
        self.resizable(False, False)
        self.username = None
        self.is_server = None
        self.partner_ip = None

        self.start_screen()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def start_screen(self):
        self.clear_widgets()
        label = ctk.CTkLabel(self, text="MathHurdle", font=("Helvetica", 48), text_color="#ffffff")
        label.place(relx=0.5, rely=0.5, anchor="center")
        self.after(2000, self.main_screen)

    def main_screen(self):
        self.clear_widgets()

        label = ctk.CTkLabel(self, text="Enter your name:", font=("Helvetica", 24))
        label.pack(pady=50)

        self.name_entry = ctk.CTkEntry(self, font=("Helvetica", 20))
        self.name_entry.pack(pady=10)

        submit_btn = ctk.CTkButton(self, text="Submit", command=self.save_name)
        submit_btn.pack(pady=20)

    def save_name(self):
        name = self.name_entry.get().strip()
        if name:
            self.username = name
            self.show_main_menu()

    def show_main_menu(self):
        self.clear_widgets()

        welcome = ctk.CTkLabel(self, text=f"Welcome, {self.username}", font=("Helvetica", 26))
        welcome.pack(pady=50)

        show_ip_btn = ctk.CTkButton(self, text="Show IP", command=self.show_ip_screen)
        show_ip_btn.pack(pady=20)

        enter_ip_btn = ctk.CTkButton(self, text="Enter IP", command=self.enter_ip_screen)
        enter_ip_btn.pack(pady=20)

    def show_ip_screen(self):
        self.is_server = True
        self.clear_widgets()

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        ip_label_1 = ctk.CTkLabel(self, text="Your IP Address Is:", font=("Helvetica", 20))
        ip_label_1.pack(pady=20)

        ip_label_2 = ctk.CTkLabel(self, text=ip_address, font=("Helvetica", 24))
        ip_label_2.pack(pady=10)

        go_back_btn = ctk.CTkButton(self, text="Go Back", command=self.show_main_menu)
        go_back_btn.pack(pady=40)

        # TODO (UDP Dev): Add logic to wait for incoming connection request here.
        # When a connection request is received, call:
        # self.handle_connection_request("partner_ip_here")

        # For now, simulate a connection request after 3 seconds
        threading.Thread(target=self.simulate_connection_request, daemon=True).start()

    def simulate_connection_request(self):
        time.sleep(3)
        self.partner_ip = "192.168.1.99"
        self.handle_connection_request(self.partner_ip)

    def handle_connection_request(self, partner_ip):
        def accept():
            self.partner_ip = partner_ip
            # TODO (UDP Dev): Send acceptance back to client
            self.show_start_screen()

        def reject():
            # TODO (UDP Dev): Notify client of rejection
            self.show_main_menu()

        response = ctk.CTkToplevel(self)
        response.geometry("400x200")
        response.title("Connection Request")

        msg = ctk.CTkLabel(response, text="Someone wants to play with you.", font=("Helvetica", 18))
        msg.pack(pady=20)

        accept_btn = ctk.CTkButton(response, text="Accept", fg_color="green", command=lambda: [response.destroy(), accept()])
        accept_btn.pack(pady=10)

        reject_btn = ctk.CTkButton(response, text="Reject", fg_color="red", command=lambda: [response.destroy(), reject()])
        reject_btn.pack(pady=10)

    def enter_ip_screen(self):
        self.is_server = False
        self.clear_widgets()

        label = ctk.CTkLabel(self, text="Enter Opponent's IP:", font=("Helvetica", 20))
        label.pack(pady=20)

        self.ip_entry = ctk.CTkEntry(self, font=("Helvetica", 18))
        self.ip_entry.pack(pady=10)

        connect_btn = ctk.CTkButton(self, text="Connect", command=self.send_connection_request)
        connect_btn.pack(pady=20)

        go_back_btn = ctk.CTkButton(self, text="Go Back", command=self.show_main_menu)
        go_back_btn.pack(pady=40)

    def send_connection_request(self):
        ip = self.ip_entry.get().strip()
        if ip:
            self.partner_ip = ip
            self.show_waiting_screen()

            # TODO (UDP Dev): Send connection request to server
            # Simulate server accepting after 3 seconds
            threading.Thread(target=self.simulate_server_acceptance, daemon=True).start()

    def simulate_server_acceptance(self):
        time.sleep(3)
        self.connection_accepted()

    def show_waiting_screen(self):
        self.clear_widgets()
        label = ctk.CTkLabel(self, text="Waiting to be connected...", font=("Helvetica", 22))
        label.pack(pady=100)

        go_back_btn = ctk.CTkButton(self, text="Go Back", command=self.show_main_menu)
        go_back_btn.pack(pady=40)

    def connection_accepted(self):
        if self.is_server:
            self.show_start_screen()
        else:
            self.show_client_wait_screen()

    def show_start_screen(self):
        self.clear_widgets()
        label = ctk.CTkLabel(self, text="Ready to Start!", font=("Helvetica", 26))
        label.pack(pady=50)

        start_btn = ctk.CTkButton(self, text="Start", command=self.start_game_placeholder)
        start_btn.pack(pady=20)

        go_back_btn = ctk.CTkButton(self, text="Go Back", command=self.show_main_menu)
        go_back_btn.pack(pady=40)

    def show_client_wait_screen(self):
        self.clear_widgets()
        label = ctk.CTkLabel(self, text="Waiting for the match to be started.", font=("Helvetica", 22))
        label.pack(pady=100)

        go_back_btn = ctk.CTkButton(self, text="Go Back", command=self.show_main_menu)
        go_back_btn.pack(pady=40)

    def start_game_placeholder(self):
        messagebox.showinfo("Game Start", "This is where the game will begin!")
        # TODO: Transition to game module


if __name__ == "__main__":
    app = MathHurdleApp()
    app.mainloop()