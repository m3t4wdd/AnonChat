import key, socket, threading, json, base64
import enc_dec_msg as encryption
from key_window import KeyWindow
from main_GUI import MainGUI

class KeyManager:

    """Manage key generation and management"""
    
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


class Client:

    """Manages server connection and communication"""

    def __init__(self, app):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.app = app

    def connect_to_server(self):
        try:
            self.client_socket.connect(("127.0.0.1", 5555))
            print("Connected to the server!")
        except Exception:
            print(f"Connection to the server failed!")

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

                dec_msg = encryption.decrypt_message(cypher, priv_key).decode('utf-8')[2:-1].strip("\x00")
                self.app.receive_message(dec_msg)

            except:
                break

if __name__ == "__main__":
    key_manager = KeyManager()
    client = Client(None)
    app = MainGUI(client, key_manager)
    client.app = app

    key_window = KeyWindow(key_manager)
    key_window.display_key_window()
    app.display_chat_window()
