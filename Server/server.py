import socket, json, threading
import peers.tables as tables

class Server:

    """Manage every connected server"""

    def handle_client(self, client_socket, clients, addr):
        try:
            while True:

                message = client_socket.recv(1024).decode("utf-8")

                if not message:
                    print("client removed: " + str(addr))
                    if client_socket in clients:
                        tables.del_peer(tuple(addr))
                        clients.remove(client_socket)
                        client_socket.close()
                    break



                if message.startswith('{"ip":') and message.endswith('}'):
                    #message = message.replace("\x00", "")
                    data = json.loads(message)
                    key = data["key"]

                    tables.add_peer(addr, key)

                # A client wants to deliver a message
                elif message.startswith('{"msg":') and message.endswith('}'):
                    data = json.loads(message)
                    
                    # get cypher and send to proper dst
                    cypher_b64, key = (data["msg"]), data["key"].replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace("\n", "")
                    sock = tables.get_ip_port(key)

                    if sock is None:
                        print(f"No peer found for the key: {key}")
                        continue
                    else:
                        target_ip, target_port = sock
                    
                        for client in clients:
                                raddr = client.getpeername()  # Returns a tuple (ip, port)
                                # Compare raddr with target IP and port
                                if raddr == (target_ip, target_port):
                                    client.sendall(str(cypher_b64).encode("utf-8"))
                                    break 
        except Exception as e:
            print(f"Error: {str(e)}")

    def start_server(self):      
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 5555))
        server.listen(5)
        print("listening...\n\n")

        clients  = []
        clients_lock = threading.Lock()

            
        while True:
            client_socket, addr = server.accept()
            print(f"Connection from {addr}")
            with clients_lock:  # Protection while adding
                clients.append(client_socket)
                
            # Create a thread as soon as a client connect
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, clients, addr))
            client_thread.start()

    
if __name__ == "__main__":
    server = Server()
    server.start_server()
