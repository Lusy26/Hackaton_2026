import os
import queue
import socket
import subprocess
import sys
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

# --------- INICIAR MAIN2 ---------
script_dir = os.path.dirname(os.path.abspath(__file__))
main2_path = os.path.join(script_dir, "main2.py")
try:
    subprocess.Popen([sys.executable, main2_path], cwd=script_dir)
except Exception as e:
    print(f"Error al ejecutar main2.py: {e}")

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
def append_chat(text):
    chat.insert(tk.END, text)
    chat.see(tk.END)


def recibir():
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                ventana.after(0, append_chat, "Conexión cerrada por el servidor\n")
                break

            mensaje = msg.decode()
            ventana.after(0, append_chat, "Servidor: " + mensaje + "\n")
        except Exception as e:
            ventana.after(0, append_chat, f"Error al recibir: {e}\n")
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