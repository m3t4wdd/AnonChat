from tkinter import Tk, Frame, Label, Button, Entry, Scrollbar, Canvas, messagebox
import json, base64, vlc
from datetime import datetime
import enc_dec_msg as encryption

class MainGUI:

    """Handle GUI and Chat logic"""

    def __init__(self, client, key_manager):
        self.client = client
        self.key_manager = key_manager

    def display_chat_window(self):
        self.chat_window = Tk()
        self.chat_window.title("AnonChat")
        self.chat_window.geometry("500x600")
        self.chat_window.configure(bg="#1F1F1F")
        self.chat_window.resizable(False, False)

        # Header
        Label(self.chat_window, text="AnonChat", font=("Arial", 21, "bold"), bg="#1F1F1F", fg="#7AF036").pack(pady=10)

        # Chat Frame with Scrollbar
        self.chat_frame = Frame(self.chat_window, bg="#1F1F1F")
        self.chat_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.canvas = Canvas(self.chat_frame, bg="#1F1F1F", highlightthickness=0)
        self.scrollbar = Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#1F1F1F")

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((100, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Input Frame
        frame = Frame(self.chat_window, bg="#2E2E2E", padx=10, pady=10)
        frame.pack(pady=10, padx=20, fill="x")

        # Public Key Entry
        Label(frame, text="Receiver's Public Key:", font=("Arial", 10, "bold"), bg="#2E2E2E", fg="#FFFFFF").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_key = Entry(frame, width=40, bg="#1F1F1F", fg="#FFFFFF", font=("Arial", 10), insertbackground="#FFFFFF")
        self.entry_key.grid(row=0, column=1, padx=5, pady=5)

        # Message Entry
        Label(frame, text="Message:", font=("Arial", 10, "bold"), bg="#2E2E2E", fg="#FFFFFF").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_msg = Entry(frame, width=40, bg="#1F1F1F", fg="#FFFFFF", font=("Arial", 10), insertbackground="#FFFFFF")
        self.entry_msg.grid(row=1, column=1, padx=5, pady=5)

        # Send Button
        Button(frame, text="Send", font=("Arial", 12, "bold"), bg="#4CAF50", fg="#FFFFFF", activebackground="#45A049", activeforeground="#FFFFFF", relief="flat", cursor="hand2", command=self.send_message).grid(row=2, column=0, columnspan=2, pady=10)

        # Connect to server
        self.client.connect_to_server()

        self.display_message("Session created, you can message now!", sender="other")

        self.chat_window.mainloop()
        self.key_manager.clear_private_key()

    def display_message(self, message, sender="me"):

        """Display a message in the chat"""

        time = datetime.now().strftime("%H:%M")
        bubble_color = "#4CAF50" if sender == "me" else "#333333"
        text_color = "#FFFFFF"

        bubble = Frame(self.scrollable_frame, bg=bubble_color, padx=10, pady=5)
        bubble.pack(anchor="e" if sender == "me" else "w", pady=5, padx=10)

        Label(bubble, text=message, font=("Arial", 10), bg=bubble_color, fg=text_color, wraplength=300, justify="left").pack()
        Label(bubble, text=time, font=("Arial", 8), bg=bubble_color, fg="#B3B3B3", anchor="e").pack(anchor="e")
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    def check_msg(self, msg):
        if len(msg) == 0:
            return "Message cannot be empty."
        if len(msg) > 500:
            return "500 character limit exceeded."
        if not msg.isprintable():
            return "Message contains invalid characters."

    def check_key(self, key):
        if len(key) < 500 or len(key) > 700:
            return "Invalid Key"
        try:
            base64.b64decode(str(key).replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", ""))
        except Exception:
            return "Key is not properly Base64-encoded."

    def send_message(self):
        key = self.entry_key.get()
        key_error = self.check_key(key.strip())

        if key_error:
            messagebox.showerror("Key error!", key_error)
        else:
            msg = self.entry_msg.get().encode("utf-8")
            msg_error = self.check_msg(msg.decode("utf-8"))

            if msg_error:
                messagebox.showerror("Message error", msg_error)
            else:
                try:
                    cypher_msg = encryption.encrypt_message(str(msg), base64.b64decode(key).decode("utf-8"))
                except Exception:
                    messagebox.showerror("Error", "Error during encryption of the message!")
                    return

                msg64 = base64.b64encode(cypher_msg).decode("utf-8")

                if key and msg.strip() and msg != b"\x00":
                    self.display_message(msg.decode("utf-8"), sender="me")

                    messaggio = json.dumps({"msg": msg64, "key": key})
                    self.client.send_message(messaggio)

                    self.entry_msg.delete(0, "end")

    def receive_message(self, message):
        p = vlc.MediaPlayer("file/notification.mp3")
        p.play()
        self.display_message(message, sender="other")
        