# AnonChat
A simple and anonymous chat application written in Python3 using sockets and tkinter as GUI.

# About
AnonChat is a simple chat application written using sockets.
Clients connect to a server by transmitting only their IP address and the public key of the "session".

- The philosophy is that each time the program is opened, a "session" is created, and a pair of public and private keys will be generated.

- When the client is closed, these keys are permanently deleted (from both the server and the host PC), making it impossible to recover the chat history.

- Messages are transmitted in JSON format and encrypted using RSA with SHA-256 (with the receiver public key) to ensure privacy and anonymity for users.

- The server will create a JSON table that connects a specific peer (IP, port) to a public key, since the server has to understand where the message has to be delivered.

What happens if 2 clients from the same intranet over NAT (so same IP), are connected to the server?
- The server will just create multiple entries with same IP but different port and public key.

- Note: The private key is only stored on the host PC and is never transmitted to the server.
Even if the message gets intercepted, it cannot be decrypted without the private key, which is stored only on the client's host PC.

# Requirements
Tkinter 8.6

# Run
- server: <code>python3 server.py</code>
- Client: <code>python3 main.py</code>

# Author
Reddit - [m3t4d00m](https://www.reddit.com/user/METRWD/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)

# Screenshots
![KeyManager](https://github.com/user-attachments/assets/632f5af4-bb4c-4703-a364-e5a276324b83)
![MainGui](https://github.com/user-attachments/assets/68f214d8-1488-4d93-bf59-f01a16a72bd0)


