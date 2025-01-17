# AnonChat
A simple and anonymous chat application written in Python3 using sockets

# About
AnonChat is a simple chat application written using sockets. Clients connect to a server by transmitting only their IP address and the public key of the "session."

The philosophy is that each time the program is opened, a "session" is created, a pair of public and private keys. When the client is closed, these keys are permanently deleted (both from the server and the host PC), making it impossible to recover the chat history.

Messages are transmitted in JSON format and encrypted using RSA with SHA-256 (with the receiver public key) to ensure privacy and anonymity for users.

The GUI is built using Tkinter.
Server will create a json table that connect a specific peer (ip, port) to a public key, this because the server will understand who to deliver the message to

Note: The private key is only stored on the host PC and is never transmitted to the server. Even if the message is intercepted, it cannot be decrypted without the private key, which is stored only on the client's host PC.

# Requirements
Tkinter 8.6

# Run
- server: python3 server.py
- Client: python3 main.py

# Author
Reddit - [m3t4d00m](https://www.reddit.com/user/METRWD/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)

# Screenshot
![image](https://github.com/user-attachments/assets/c06ff952-d26d-4767-8227-f7a7dd531db9)
![image](https://github.com/user-attachments/assets/88f3fd75-44a2-479c-9fb4-8beb9d50f1f9)

