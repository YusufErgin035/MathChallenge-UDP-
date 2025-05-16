import customtkinter as ctk
import socket
import threading
import time
from core import Core
from tkinter import messagebox

# Setup theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# App class
class MathHurdleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MathHurdle")
        self.geometry("600x800")
        self.resizable(False, False)
        
        self.username = None
        self.client_ip = None  # For UDP partner
        self.core = Core()

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

        self.name_label = ctk.CTkLabel(self.main_frame, text="Enter Your Name:", font=("Arial", 24))
        self.name_label.pack(pady=(20, 10))

        self.name_entry = ctk.CTkEntry(self.main_frame, font=("Arial", 20))
        self.name_entry.pack(pady=(0, 20))

        self.name_button = ctk.CTkButton(self.main_frame, text="Continue", command=self.save_name)
        self.name_button.pack(pady=(0, 40))

    def save_name(self):
        name = self.name_entry.get()
        if name.strip() == "":
            messagebox.showerror("Error", "Please enter a name.")
        else:
            self.username = name
            self.show_main_menu()

    def show_main_menu(self):
        self.clear_widgets()

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(fill="both", expand=True, padx=50, pady=50)

        welcome = ctk.CTkLabel(self.menu_frame, text=f"Welcome, {self.username}", font=("Arial", 30))
        welcome.pack(pady=(20, 40))

        show_ip_btn = ctk.CTkButton(self.menu_frame, text="Show IP", command=self.show_ip_screen)
        show_ip_btn.pack(pady=20)

        enter_ip_btn = ctk.CTkButton(self.menu_frame, text="Enter IP", command=self.enter_ip_screen)
        enter_ip_btn.pack(pady=20)

    def show_ip_screen(self):
        self.clear_widgets()

        self.ip_frame = ctk.CTkFrame(self)
        self.ip_frame.pack(fill="both", expand=True, padx=50, pady=50)

        ip_text = ctk.CTkLabel(self.ip_frame, text="Your IP Address Is:", font=("Arial", 24))
        ip_text.pack(pady=(20, 10))

        # Core'dan ip çekmek
        ip_addr = self.core.get_ip()
        ip_label = ctk.CTkLabel(self.ip_frame, text=ip_addr, font=("Arial", 24))
        ip_label.pack(pady=(0, 40))

        threading.Thread(target=self.connection_request).start()

    def connection_request(self):
        time.sleep(5)
        self.ask_for_acceptance()

    def ask_for_acceptance(self, request_ip):
        def on_accept():
            self.show_start_screen()

        def on_reject():
            self.show_main_menu()

        response = messagebox.askquestion("Incoming Request", f"{request_ip} wants to play with you.\nDo you accept?")
        if response == "yes":
            self.after(100, on_accept)
        else:
            self.after(100, on_reject)

    def enter_ip_screen(self):
        self.clear_widgets()

        self.enter_ip_frame = ctk.CTkFrame(self)
        self.enter_ip_frame.pack(fill="both", expand=True, padx=50, pady=50)

        label = ctk.CTkLabel(self.enter_ip_frame, text="Enter Opponent's IP Address:", font=("Arial", 22))
        label.pack(pady=(20, 10))

        self.ip_entry = ctk.CTkEntry(self.enter_ip_frame, font=("Arial", 20))
        self.ip_entry.pack(pady=(0, 20))

        send_btn = ctk.CTkButton(self.enter_ip_frame, text="Connect", command=self.send_connection_request)
        send_btn.pack(pady=20)

    def send_connection_request(self):
        self.client_ip = self.ip_entry.get().strip()
        if self.client_ip == "":
            messagebox.showerror("Error", "Please enter a valid IP address.")
            return

        self.core.send_areuactive(self.client_ip, self.port)

        self.waiting_screen()

    def waiting_screen(self):
        self.clear_widgets()

        self.waiting_frame = ctk.CTkFrame(self)
        self.waiting_frame.pack(fill="both", expand=True, padx=50, pady=50)

        label = ctk.CTkLabel(self.waiting_frame, text="Waiting to be connected...", font=("Arial", 24))
        label.place(relx=0.5, rely=0.5, anchor="center")

        # 💬 PLACEHOLDER: After receiving "Accepted" from other side, call:
        threading.Thread(target=self.simulate_wait_and_proceed).start()

    def simulate_wait_and_proceed(self):
        while True:
            if self.core.is_active:
                break

        self.show_start_screen()

    def show_start_screen(self):
        self.clear_widgets()

        self.start_frame = ctk.CTkFrame(self)
        self.start_frame.pack(fill="both", expand=True, padx=50, pady=50)

        label = ctk.CTkLabel(self.start_frame, text="Ready to Start!", font=("Arial", 28))
        label.pack(pady=40)

        start_btn = ctk.CTkButton(self.start_frame, text="Start", font=("Arial", 24))
        start_btn.pack(pady=20)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

# Run the app
if __name__ == "__main__":
    app = MathHurdleApp()
    app.mainloop()