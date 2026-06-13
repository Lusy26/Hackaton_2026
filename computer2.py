import os
import queue
import socket
import subprocess
import sys
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

script_dir = os.path.dirname(os.path.abspath(__file__))
main2_path = os.path.join(script_dir, "main2.py")

# --------- SOCKET ---------
HOSTS = ["10.10.11.204", "127.0.0.1", "localhost"]
PORT = 12345

client = socket.socket()
connected_ok = False
last_error = None
child_process = None
for host in HOSTS:
    try:
        client.connect((host, PORT))
        HOST = host
        connected_ok = True
        break
    except Exception as e:
        last_error = e

if not connected_ok:
    print(f"Error al conectar con {HOSTS}: {last_error}")

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

def launch_game(seed):
    global child_process
    if child_process and child_process.poll() is None:
        ventana.after(0, append_chat, "El juego ya se está ejecutando\n")
        return

    if os.path.exists(main2_path):
        try:
            child_process = subprocess.Popen([sys.executable, main2_path, str(seed)], cwd=script_dir)
            ventana.after(0, append_chat, f"Juego iniciado con seed: {seed}\n")
        except Exception as e:
            ventana.after(0, append_chat, f"Error al ejecutar main2.py: {e}\n")
    else:
        ventana.after(0, append_chat, "No se encontró main2.py\n")


def ask_seed_for_game():
    seed_win = tk.Toplevel(ventana)
    seed_win.title("Seed para laberinto")

    tk.Label(seed_win, text="Ingrese seed:").pack(padx=10, pady=5)
    seed_entry = tk.Entry(seed_win)
    seed_entry.pack(padx=10, pady=5)
    seed_entry.focus_set()

    def on_ok(event=None):
        seed_value = seed_entry.get().strip()
        if seed_value == "":
            seed_value = "0"
        seed_win.destroy()
        launch_game(seed_value)

    tk.Button(seed_win, text="Iniciar juego", command=on_ok).pack(padx=10, pady=10)
    seed_win.bind("<Return>", on_ok)
    seed_win.transient(ventana)
    seed_win.grab_set()


if connected_ok:
    ventana.after(0, append_chat, f"Conectado a servidor en {HOST}:{PORT}\n")
    ventana.after(0, append_chat, "Ingrese el seed para el laberinto.\n")
    ventana.after(0, ask_seed_for_game)
    threading.Thread(target=recibir, daemon=True).start()
else:
    ventana.after(0, append_chat, f"No se pudo conectar con el servidor {HOSTS}: {last_error}\n")

# --------- ENVIAR MENSAJES ---------
def enviar(event=None):
    if not connected_ok:
        chat.insert(tk.END, "No hay conexión al servidor\n")
        return

    msg = entrada.get()
    try:
        client.send(msg.encode())
    except Exception as e:
        chat.insert(tk.END, f"Error al enviar: {e}\n")
        return

    chat.insert(tk.END, "Tú: " + msg + "\n")
    entrada.delete(0, tk.END)

entrada.bind("<Return>", enviar)

boton = tk.Button(ventana, text="Enviar", command=enviar)
boton.pack()

ventana.mainloop()

client.close()