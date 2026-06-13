import os
import socket
import subprocess
import sys
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
child_process = None

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
    chat.insert(tk.END, f"Clie5
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

# --------- EJECUTAR main.py ---------
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(script_dir, "main1.py")

    if os.path.exists(main_path):
        try:
            child_process = subprocess.Popen([sys.executable, main_path], cwd=script_dir)
        except Exception as e:
            chat.insert(tk.END, f"Error al ejecutar main1.py: {e}\n")
    else:
        chat.insert(tk.END, "No se encontró main1.py\n")

    def on_close():
        global child_process

        if child_process and child_process.poll() is None:
            child_process.terminate()
            try:
                child_process.wait(timeout=5)
            except Exception:
                pass

        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", on_close)
    ventana.mainloop()