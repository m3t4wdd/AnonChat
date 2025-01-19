from tkinter import Tk, Frame, Label, Text, Button

class KeyWindow:
    def __init__(self, key_manager):
        self.key_manager = key_manager

    def display_key_window(self):
        self.key_manager.generate_keys()

        self.key_window = Tk()
        self.key_window.title("AnonChat")
        self.key_window.geometry("500x600")
        self.key_window.resizable(True, True)

        frame = Frame(self.key_window, bg="lightgrey", padx=10, pady=10)
        frame.pack(pady=20)

        def copy_to_clipboard(dtxt):
            self.key_window.clipboard_clear()
            self.key_window.clipboard_append(dtxt)
            label2.config(text="Public Key Copied")

        Label(frame, text="Public Key:", font=("Arial", 10, "bold"), bg="lightgrey").pack(anchor="w", padx=10, pady=(10, 0))
        pub_box = Text(frame, wrap="word", height=5, width=70)
        pub_box.insert("1.0", self.key_manager.pub_key)
        pub_box.pack(padx=10, pady=5)
        pub_box.config(state="disabled")

        Button(frame, text='Copy', relief="raised", bd=3, cursor="hand2", command=lambda: copy_to_clipboard(self.key_manager.pub_key)).pack()

        label2 = Label(frame, font=("Arial", 10, "bold"), fg="blue", bg="lightgrey", justify="left")
        label2.pack(anchor="center", padx=10, pady=(10, 0))

        label = Label(frame, text="WARNING!\n\n- Upon closing the program, the keys (public and private) will be irreversibly changed, rendering the conversation inaccessible:", font=("Arial", 10, "bold"), fg="red", bg="lightgrey", justify="left")
        label.pack(anchor="center", padx=10, pady=(10, 0))
        label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))

        Button(self.key_window, text="Start Chat", command=self.key_window.destroy, relief="raised", bd=3, cursor="hand2").pack(pady=10)

        self.key_window.mainloop()