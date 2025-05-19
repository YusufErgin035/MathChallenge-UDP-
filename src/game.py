import json
import tkinter as tk
import random
import threading
import time

def send_data(core,question_data,isAnswer,answer):
    data = {
        "status": 0,
        "func": 3,
        "msg_id": random.randint(1000, 9999),
        "msg": {
            "isAnswer": isAnswer,
            "question": question_data,
            "answer": answer
        }
    }
    core.conn.send(core.target_ip, core.target_port, json.dumps(data))

def notify_opponent_disconnected(core):
    data = {
        "status": -1,
        "func": -1,
        "msg_id": -1,
    }
    core.conn.send(core.target_ip, core.target_port, json.dumps(data))

class Game:
    def __init__(self, root, player_name, is_server,core):
        self.receive_notice_data = self.receive_notice_data
        self.root = root
        self.player_name = player_name
        self.is_server = is_server
        self.opponent_name = "Opponent"
        self.score = {"me": 0, "opponent": 0}
        self.current_question = 1
        self.answer = None
        self.question = None
        self.has_answered = False
        self.max_score = 5
        self.answer_buttons = []
        self.correct_answer = None
        self.core = core
        self.core.on_game_data_callback = self.receive_game_data

        self.root.protocol("WM_DELETE_WINDOW", self.exit_game())
        self.create_game_screen()
        self.show_countdown()

    def receive_notice_data(self, core):
        print("Rakip oyundan çıktı..")
        self.force_to_exit()

    def receive_game_data(self, is_answer, question, answer):
        print("Karşıdan veri geldi:", is_answer, question, answer)
        if is_answer:
            self.handle_answer(answer,True)
        if not is_answer and question:
            self.question = question
            self.answer = answer
            self.generate_question(self.is_server)

    def create_game_screen(self):
        self.clear_screen()
        self.root.configure(bg="black")
        self.status_label = tk.Label(self.root, text="", fg="white", bg="black", font=("Helvetica", 24))
        self.status_label.pack(pady=20)

        self.score_label = tk.Label(self.root,text=f"Score: {self.score['me']} - {self.score['opponent']}",fg="white", bg="black",font=("Helvetica", 18))
        self.score_label.pack(pady=10)

        self.question_label = tk.Label(self.root, text="", fg="white", bg="black", font=("Helvetica", 22))
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(self.root, bg="black")
        self.options_frame.pack()

        self.exit_button = tk.Button(self.root, text="Exit Game", bg="red", fg="white", font=("Helvetica", 14), command=self.exit_game)
        self.exit_button.pack(pady=30)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_countdown(self):
        self.clear_screen()
        self.root.configure(bg="black")
        count_label = tk.Label(self.root, text="", fg="white", bg="black", font=("Helvetica", 48))
        count_label.pack(pady=100)

        def countdown():
            for i in ["3", "2", "1"]:
                count_label.config(text=i)
                time.sleep(1)
            count_label.config(text=f"Question {self.current_question}")
            time.sleep(1)
            self.create_game_screen()
            self.has_answered = False
            self.generate_question(self.is_server)

        threading.Thread(target=countdown).start()

    def generate_question(self,isHost):
        if isHost:
            expression_parts = [str(random.randint(1, 20))]
            for _ in range(random.randint(2, 4)):
                op = random.choice(['+', '-', '*'])
                num = str(random.randint(1, 20))
                expression_parts.extend([op, num])
            question = ' '.join(expression_parts)
            self.correct_answer = eval(question)
            self.question_label.config(text=question)

            wrong_answers = set()
            while len(wrong_answers) < 3:
                wrong = self.correct_answer + random.choice([-10, -5, -2, 2, 5, 10])
                if wrong != self.correct_answer:
                    wrong_answers.add(wrong)

            options = list(wrong_answers) + [self.correct_answer]
            random.shuffle(options)
            send_data(self.core,question,False,options)
        else:
            if not self.question or not self.answer:
                print("Soru veya cevap listesi eksik.")
                return
            self.correct_answer = eval(self.question)
            options = list(self.answer)
            random.shuffle(options)
            self.question_label.config(text=self.question)

        for btn in self.answer_buttons:
            btn.destroy()

        self.answer_buttons = []
        for i, option in enumerate(options):
            btn = tk.Button(
                self.options_frame,
                text=str(option),
                width=15,
                height=3,
                bg="#444",
                fg="white",
                font=("Helvetica", 16),
                command=lambda val=option: self.handle_answer(val,False)
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
            self.answer_buttons.append(btn)

    def handle_answer(self, selected_answer,isOpponent):
        if self.has_answered:
            return
        self.has_answered = True

        if not isOpponent:
            is_correct = selected_answer == self.correct_answer
            self.score["me" if is_correct else "opponent"] += 1
            send_data(self.core, None, True, selected_answer)
            message = f"{self.player_name} has given {'the correct' if is_correct else 'a wrong'} answer."
        else:
            is_correct = selected_answer == self.correct_answer
            self.score["opponent" if is_correct else "me"] += 1
            message = f"{self.opponent_name} has given {'the correct' if is_correct else 'a wrong'} answer."

        self.announce_result(message)

        if self.score["me"] == self.max_score:
            self.root.after(2000, lambda: self.end_game("Victory"))
        elif self.score["opponent"] == self.max_score:
            self.root.after(2000, lambda: self.end_game("Lose"))
        else:
            self.current_question += 1
            self.has_answered = False
            self.root.after(2000, self.show_countdown)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score['me']} - {self.score['opponent']}")

    def announce_result(self, message):
        self.clear_screen()
        label = tk.Label(self.root, text=message, fg="white", bg="black", font=("Helvetica", 28))
        label.pack(pady=50)
        score = tk.Label(self.root, text=f"{self.score['me']} - {self.score['opponent']}", fg="white", bg="black", font=("Helvetica", 20))
        score.pack(pady=20)

        self.root.after(2000, self.create_game_screen)

    def end_game(self, result):
        self.clear_screen()
        result_text = "Victory" if result == "Victory" else "Lose"
        label = tk.Label(self.root, text=result_text, fg="green" if result == "Victory" else "red", bg="black", font=("Helvetica", 36))
        label.pack(pady=30)

        final = tk.Label(self.root, text=f"{self.player_name} has won." if result == "Victory" else f"{self.opponent_name} has won.", fg="white", bg="black", font=("Helvetica", 20))
        final.pack(pady=20)

    def force_to_exit(self):
        self.clear_screen()
        label = tk.Label(self.root, text="Opponent has left. You win!", fg="white", bg="black", font=("Helvetica", 24))
        label.pack(pady=100)
        self.exit_button = tk.Button(self.root, text="Exit Game", bg="red", fg="white", font=("Helvetica", 14),command=self.root.destroy)
        self.exit_button.pack(pady=30)

    def exit_game(self):
        self.clear_screen()
        notify_opponent_disconnected(self.core)
        self.root.destroy()


