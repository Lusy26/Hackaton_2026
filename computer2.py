import socket

HOST = "10.10.11.204"
PORT = 12345

client = socket.socket()
client.connect((HOST, PORT))

print("Conectado al servidor")

while True:
    msg = input("Tú: ")

    client.send(msg.encode())

    respuesta = client.recv(1024).decode()

    print("Servidor:", respuesta)