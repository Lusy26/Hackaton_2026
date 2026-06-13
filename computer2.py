import socket
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

# --------- SOCKET ---------
HOST = "10.10.11.204"
PORT = 12345

client = socket.socket()
client.connect((HOST, PORT))

# --------- VENTANA ---------
ventana = tk.Tk()
ventana.title("Chat")

chat = ScrolledText(ventana, width=50, height=20)
chat.pack()

entrada = tk.Entry(ventana, width=40)
entrada.pack()

# --------- RECIBIR MENSAJES ---------
def recibir():
    while True:
        try:
            msg = client.recv(1024).decode()
            chat.insert(tk.END, "Servidor: " + msg + "\n")
        except:
            break

threading.Thread(target=recibir, daemon=True).start()

# --------- ENVIAR MENSAJES ---------
def enviar(event=None):
    msg = entrada.get()
    client.send(msg.encode())

    chat.insert(tk.END, "Tú: " + msg + "\n")
    entrada.delete(0, tk.END)

entrada.bind("<Return>", enviar)

boton = tk.Button(ventana, text="Enviar", command=enviar)
boton.pack()

ventana.mainloop()

client.close()