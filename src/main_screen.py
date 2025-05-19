import customtkinter as ctk
import socket
import threading
from core import Core
from tkinter import messagebox
from game import Game
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class MathHurdleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.ip_entry = None
        self.title("MathHurdle")
        self.geometry("600x800")
        self.resizable(False, False)

        self.username = None
        self.client_ip = None
        self.is_server = None
        self.core = Core()
        self.core.on_game_request_callback = self.handle_game_request  # 🔗 Bağlantı kuruldu

        self.show_intro_screen()

    def show_intro_screen(self):
        self.intro_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.intro_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self.intro_frame, text="MathHurdle", font=("Arial", 60), text_color="#FFFFFF")
        title.place(relx=0.5, rely=0.5, anchor="center")

        self.after(2000, self.show_main_screen)

    def show_main_screen(self):
        self.clear_widgets()

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=50, pady=50)

        name_label = ctk.CTkLabel(self.main_frame, text="Enter Your Name:", font=("Arial", 24))
        name_label.pack(pady=(20, 10))

        self.name_entry = ctk.CTkEntry(self.main_frame, font=("Arial", 20))
        self.name_entry.pack(pady=(0, 20))

        name_button = ctk.CTkButton(self.main_frame, text="Continue", command=self.save_name)
        name_button.pack(pady=(0, 40))

    def save_name(self):
        name = self.name_entry.get()
        if name.strip() == "":
            messagebox.showerror("Error", "Please enter a name.")
        else:
            self.username = name
            self.show_main_menu()

    def show_main_menu(self):
        self.clear_widgets()

        menu_frame = ctk.CTkFrame(self)
        menu_frame.pack(fill="both", expand=True, padx=50, pady=50)

        welcome = ctk.CTkLabel(menu_frame, text=f"Welcome, {self.username}", font=("Arial", 30))
        welcome.pack(pady=(20, 40))

        show_ip_btn = ctk.CTkButton(menu_frame, text="Show IP", command=self.show_ip_screen)
        show_ip_btn.pack(pady=20)

        enter_ip_btn = ctk.CTkButton(menu_frame, text="Enter IP", command=self.enter_ip_screen)
        enter_ip_btn.pack(pady=20)

    def show_ip_screen(self):
        self.clear_widgets()
        self.is_server = True

        ip_frame = ctk.CTkFrame(self)
        ip_frame.pack(fill="both", expand=True, padx=50, pady=50)

        ip_text = ctk.CTkLabel(ip_frame, text="Your IP Address Is:", font=("Arial", 24))
        ip_text.pack(pady=(20, 10))

        ip_addr = self.core.get_ip()
        ip_label = ctk.CTkLabel(ip_frame, text=ip_addr, font=("Arial", 24))
        ip_label.pack(pady=(0, 40))

    def handle_game_request(self):
        self.after(0, self.ask_game_accept)

    def ask_game_accept(self):
        response = messagebox.askquestion("Incoming Request", "Someone wants to play with you.\nDo you accept?")
        if response == "yes":
            self.show_start_screen()
        else:
            self.show_main_menu()

    def enter_ip_screen(self):
        self.clear_widgets()
        self.is_server = False

        enter_ip_frame = ctk.CTkFrame(self)
        enter_ip_frame.pack(fill="both", expand=True, padx=50, pady=50)

        label = ctk.CTkLabel(enter_ip_frame, text="Enter Opponent's IP Address:", font=("Arial", 22))
        label.pack(pady=(20, 10))

        self.ip_entry = ctk.CTkEntry(enter_ip_frame, font=("Arial", 20))
        self.ip_entry.pack(pady=(0, 20))

        send_btn = ctk.CTkButton(enter_ip_frame, text="Connect", command=self.send_connection_request)
        send_btn.pack(pady=20)

    def send_connection_request(self):
        self.client_ip = self.ip_entry.get().strip()
        if self.client_ip == "":
            messagebox.showerror("Error", "Please enter a valid IP address.")
            return

        self.core.send_areuactive(self.client_ip)

        self.clear_widgets()

        waiting_frame = ctk.CTkFrame(self)
        waiting_frame.pack(fill="both", expand=True, padx=50, pady=50)

        label = ctk.CTkLabel(waiting_frame, text="Waiting to be connected...", font=("Arial", 24))
        label.place(relx=0.5, rely=0.5, anchor="center")

        threading.Thread(target=self.client_simulate_wait_and_proceed, daemon=True).start()

    def client_simulate_wait_and_proceed(self):
        while not self.core.is_active:
            pass

        self.core.send_game_request()

        while not self.core.is_game_request:
            pass

        while not self.core.is_game_accepted:
            pass

        while not self.core.is_game_started:
            pass

        self.start_game()

    def show_start_screen(self):
        self.clear_widgets()

        self.core.send_accept_game_request()

        start_frame = ctk.CTkFrame(self)
        start_frame.pack(fill="both", expand=True, padx=50, pady=50)

        label = ctk.CTkLabel(start_frame, text="Ready to Start!", font=("Arial", 28))
        label.pack(pady=40)

        start_btn = ctk.CTkButton(start_frame, text="Start", font=("Arial", 24), command=self.start_game)
        start_btn.pack(pady=20)

    def start_game(self):
        self.core.send_game_start()

        root = tk.Tk()
        root.title("Math Hurdle - Game")
        root.geometry("600x800")
        root.configure(bg="black")

        Game(root, self.username, self.is_server)
        root.mainloop()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = MathHurdleApp()
    app.mainloop()
