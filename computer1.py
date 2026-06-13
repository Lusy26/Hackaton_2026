import socket

HOST = "0.0.0.0"
PORT = 12345

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("Servidor encendido... esperando cliente")

conn, addr = server.accept()
print("Cliente conectado:", addr)

while True:
    data = conn.recv(1024).decode()

    if not data:
        break

    print("Cliente:", data)

    respuesta = input("Tú: ")
    conn.send(respuesta.encode())