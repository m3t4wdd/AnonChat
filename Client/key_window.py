from tkinter import Tk, Frame, Label, Text, Button

class KeyWindow:
    def __init__(self, key_manager):
        self.key_manager = key_manager

    def display_key_window(self):
        self.key_manager.generate_keys()

        # Finestra principale
        self.key_window = Tk()
        self.key_window.title("AnonChat - Key")
        self.key_window.geometry("500x600")
        self.key_window.resizable(True, True)
        self.key_window.configure(bg="#1F1F1F")  # Sfondo scuro per un design moderno

        # Frame principale
        frame = Frame(self.key_window, bg="#2E2E2E", padx=20, pady=20)  # Sfondo grigio scuro per il frame
        frame.pack(pady=20, padx=10)

        # Funzione per copiare nella clipboard
        def copy_to_clipboard(dtxt):
            self.key_window.clipboard_clear()
            self.key_window.clipboard_append(dtxt)
            label2.config(text="Public Key Copied", fg="#4CAF50")

        # Titolo e Box per la Public Key
        Label(frame, text="Public Key:", font=("Arial", 12, "bold"), bg="#2E2E2E", fg="#FFFFFF").pack(anchor="w", pady=(10, 5))
        pub_box = Text(frame, wrap="word", height=5, width=60, bg="#1F1F1F", fg="#FFFFFF", font=("Arial", 10), relief="flat", highlightthickness=1)
        pub_box.insert("1.0", self.key_manager.pub_key)
        pub_box.pack(pady=5, padx=10)
        pub_box.config(state="disabled")

        # Bottone per copiare
        Button(frame, text='Copy', font=("Arial", 10, "bold"), bg="#4CAF50", fg="#FFFFFF", activebackground="#45A049", activeforeground="#FFFFFF", cursor="hand2", relief="flat", command=lambda: copy_to_clipboard(self.key_manager.pub_key)).pack(pady=(5, 10))

        # Messaggio di stato
        label2 = Label(frame, text="", font=("Arial", 10), bg="#2E2E2E", fg="#FFFFFF", justify="center")
        label2.pack(anchor="center", pady=(5, 10))

        # Avviso
        label = Label(
            frame, 
            text="WARNING!\n\n- Upon closing the program, the keys (public and private) will be irreversibly changed, making the conversation inaccessible.", 
            font=("Arial", 10, "bold"), 
            fg="#FF4C4C", 
            bg="#2E2E2E", 
            justify="left",
            wraplength=400
        )
        label.pack(anchor="center", pady=(10, 20))

        # Bottone "Start Chat"
        Button(self.key_window, text="Start Chat", font=("Arial", 12, "bold"), bg="#4CAF50", fg="#FFFFFF", activebackground="#45A049", activeforeground="#FFFFFF", cursor="hand2", relief="flat", command=self.key_window.destroy).pack(pady=20)

        self.key_window.mainloop()
