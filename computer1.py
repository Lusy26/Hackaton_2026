import socket
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

# --------- SOCKET ---------
HOST = "0.0.0.0"
PORT = 12345

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

conn = None

# --------- VENTANA ---------
ventana = tk.Tk()
ventana.title("Servidor Chat")

chat = ScrolledText(ventana, width=50, height=20)
chat.pack()

entrada = tk.Entry(ventana, width=40)
entrada.pack()

# --------- ESPERAR CLIENTE ---------
def aceptar():
    global conn

    conn, addr = server.accept()
    chat.insert(tk.END, f"Cliente conectado: {addr}\n")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            chat.insert(tk.END, "Cliente: " + data + "\n")
        except:
            break

threading.Thread(target=aceptar, daemon=True).start()

# --------- ENVIAR MENSAJES ---------
def enviar(event=None):
    msg = entrada.get()

    if conn:
        conn.send(msg.encode())

    chat.insert(tk.END, "Tú: " + msg + "\n")
    entrada.delete(0, tk.END)

entrada.bind("<Return>", enviar)

boton = tk.Button(ventana, text="Enviar", command=enviar)
boton.pack()

ventana.mainloop()