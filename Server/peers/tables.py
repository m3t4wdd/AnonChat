import json

global path
path = "peers/tables.json"

def add_peer(new_ip, new_key):
    with open(path, "r") as file:
        data = json.load(file)
    
    # Add new peer
    new_peer = {"ip": new_ip, "public_key": new_key}
    data["peers"].append(new_peer)
    
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
    print("Peer succesfully added!")


def get_ip_port(key):
    with open(path, "r") as file:
        data = json.load(file)

    # Find peer from public key
    for peer in data["peers"]:
        if peer["public_key"] == key:
            ip, port = peer["ip"][0], peer["ip"][1]
            return ip, port
    return None


def del_peer(addr):
    ip = addr[0]
    port = addr[1]

    with open(path, "r") as file:
        data = json.load(file)

    data["peers"] = [peer for peer in data["peers"] if str(peer["ip"][0]) != str(ip) or str(peer["ip"][1]) != str(port)]

    with open(path, "w") as file:
        json.dump(data, file, indent=4)
