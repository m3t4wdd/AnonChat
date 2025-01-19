import socket, json, threading
import peers.tables as tables

# Funzione per gestire ogni client connesso
def handle_client(client_socket, clients, addr):
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                # Aggiunge peer alla tables
                if message.startswith('{"ip":') and message.endswith('}'):
                    #message = message.replace("\x00", "")
                    data = json.loads(message)
                    key = data["key"]

                    tables.add_peer(addr, key)

                # Un client vuole recapitare un messaggio
                elif message.startswith('{"msg":') and message.endswith('}'):
                    data = json.loads(message)

                    cypher_b64, key = (data["msg"]), data["key"].replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace("\n", "") #qui, ricevo cypher e devo mandare a dst
                    sock = tables.get_ip_port(key)

                    if sock is None:
                        print(f"No peer found for the key: {key}")
                        continue
                    else:
                        target_ip, target_port = sock
                    
                        for client in clients:
                                raddr = client.getpeername()  # Restituisce una tupla (ip, port)
                                # Confronta raddr con il target IP e porta
                                if raddr == (target_ip, target_port):
                                    client.sendall(str(cypher_b64).encode("utf-8"))
                                    break 
            else:
                print("client removed: " + str(addr))
                tables.del_peer(tuple(addr))
                clients.remove(client)
                client.close()

    except Exception as e:
        pass

def start_server():      
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))  # Ascolta su tutte le interfacce e porta 5555
    server.listen(5)
    print("listening...\n\n")

    clients  = []
    clients_lock = threading.Lock()

        
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        with clients_lock:  # Protezione durante l'aggiunta
            clients.append(client_socket)
            
        # Crea un thread per ogni client che si connette
        client_thread = threading.Thread(target=handle_client, args=(client_socket, clients, addr))
        client_thread.start()

    
if __name__ == "__main__":
    start_server()
