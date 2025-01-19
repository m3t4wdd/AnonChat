from tkinter import *
from tkinter import messagebox
import key, socket, threading, json, base64
from datetime import datetime
import enc_dec_msg as encryption
from key_window import KeyWindow

class KeyManager:
    """Gestisce la generazione e la gestione delle chiavi."""
    def __init__(self):
        self.pub_key = None
        self.priv_key = None

    def generate_keys(self):
        self.pub_key, self.priv_key = key.gen_key()
        with open("file/session.txt", "w") as file:
            clean_priv = self.priv_key
            file.write(clean_priv)

    def clear_private_key(self):
        with open("file/session.txt", "w") as file:
            file.write("")


class ChatApp:
    """Gestisce la GUI la logica della chat."""
    def __init__(self, client, key_manager):
        self.client = client
        self.key_manager = key_manager

    def display_chat_window(self):
        self.chat_window = Tk()
        self.chat_window.title("AnonChat")
        self.chat_window.geometry("500x600")
        self.chat_window.resizable(True, True)

        Label(text="Received:").pack()

        self.text_box = Text(self.chat_window, height=20, width=50, state="disabled")
        self.text_box.pack()

        frame = Frame(self.chat_window, bg="#C0C0C0", padx=10, pady=10)
        frame.pack(pady=20, side="bottom")

        Label(frame, text="Send message:", bg="#C0C0C0").grid(row=0, column=0, columnspan=2, padx=5, pady=10)
        Label(frame, text="Public key (receiver):", bg="#C0C0C0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_key = Entry(frame, width=30)
        self.entry_key.grid(row=1, column=1, padx=5, pady=5)

        Label(frame, text="Message:", bg="#C0C0C0").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_msg = Entry(frame, width=30)
        self.entry_msg.grid(row=2, column=1, padx=5, pady=5)

        Button(frame, text="Send", command=self.send_message, relief="raised", bd=3, cursor="hand2").grid(row=3, column=0, columnspan=2, pady=10)

        
        self.client.connect_to_server()

        self.chat_window.mainloop()

        self.key_manager.clear_private_key()

    def check_msg(self, msg):

        if (len(msg) == 0):
            return "message cannot be empty."
        if (len(msg) > 500):
            return "500 character limits exceded."
        if not msg.isprintable():
            return "character not allowed."
        
    def check_key(self, key):
        
        if len(key) < 500 or len(key) > 700:
            return "Invalid Key"
        
        '''# Verifica delimitatori PEM
        if not key.startswith("-----BEGIN PUBLIC KEY-----"):
            return "Key is invalid."
        if not key.endswith("-----END PUBLIC KEY-----"):
            return "Key is invalid."'''
        
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
                    messagebox.showerror("Error", "Error during encryption message!")
                    return
                
                msg64 = base64.b64encode(cypher_msg).decode("utf-8")

                if key and msg.strip() and msg != b"\x00":
                    time = datetime.now().strftime("%H:%M")

                    self.text_box.tag_config("mine", background="#00FF00", justify="right", rmargin=30)
                    self.text_box.config(state="normal")


                    self.text_box.insert(END, f"{msg.decode('utf-8')} | {time} \n", "mine")
                    self.text_box.config(state="disabled")

                    
                    messaggio = json.dumps({"msg": msg64, "key": key})
                    
                    self.client.send_message(messaggio)

                    self.entry_key.delete(0, END)
                    self.entry_msg.delete(0, END)

    def receive_message(self, message):
        time = datetime.now().strftime("%H:%M")
        self.text_box.config(state="normal")
        self.text_box.insert(END, f"{message.replace('\x00', '')} | {time} \n")
        self.text_box.config(state="disabled")


class Client:
    """Gestisce la connessione al server e la comunicazione."""
    def __init__(self, app):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.app = app

    def connect_to_server(self):
        try:
            self.client_socket.connect(("127.0.0.1", 5555))
            print("Connected to the server!")
        except Exception as e:
            print(f"Connection to the server failed!: {str(e)}")

        client_ip = socket.gethostbyname(socket.gethostname())
        valore = app.key_manager.pub_key.decode("utf-8")
        messaggio = json.dumps({"ip": client_ip, "key": valore})

        self.client_socket.sendall(messaggio.encode('utf-8'))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

    def send_message(self, message):
        self.client_socket.sendall(message.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                cypher = base64.b64decode(message)
                with open("file/session.txt", "r") as file:
                    priv_key = file.read()
                
                #decrypt del messaggio
                dec_msg = encryption.decrypt_message(cypher, priv_key).decode('utf-8')[2:-1].strip("\x00")

                self.app.receive_message(dec_msg)

            except:
                break


if __name__ == "__main__":
    key_manager = KeyManager()
    client = Client(None)
    app = ChatApp(client, key_manager)
    client.app = app

    key_window = KeyWindow(key_manager)
    key_window.display_key_window()
    app.display_chat_window()
