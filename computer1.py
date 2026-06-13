import os
import queue
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
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

conn = None
child_process = None
message_queue = queue.Queue()
script_dir = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.join(script_dir, "main.py")
if not os.path.exists(main_path):
    main_path = os.path.join(script_dir, "main1.py")

# --------- VENTANA ---------
ventana = tk.Tk()
ventana.title("Servidor Chat")

chat = ScrolledText(ventana, width=50, height=20)
chat.pack()

entrada = tk.Entry(ventana, width=40)
entrada.pack()

# --------- ESPERAR CLIENTE ---------
def append_chat(text):
    chat.insert(tk.END, text)
    chat.see(tk.END)


def launch_game(seed):
    global child_process
    if child_process and child_process.poll() is None:
        ventana.after(0, append_chat, "El juego ya se está ejecutando\n")
        return

    if os.path.exists(main_path):
        try:
            child_process = subprocess.Popen([sys.executable, main_path, str(seed)], cwd=script_dir)
            ventana.after(0, append_chat, f"Juego iniciado con seed: {seed}\n")
        except Exception as e:
            ventana.after(0, append_chat, f"Error al ejecutar {os.path.basename(main_path)}: {e}\n")
    else:
        ventana.after(0, append_chat, "No se encontró main.py ni main1.py\n")


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


def aceptar():
    global conn

    ventana.after(0, append_chat, "Esperando cliente en {}:{}...\n".format(HOST, PORT))
    try:
        conn, addr = server.accept()
        ventana.after(0, append_chat, f"Cliente conectado: {addr}\n")
        ventana.after(0, append_chat, "Ingrese el seed para generar el laberinto.\n")
        ventana.after(0, ask_seed_for_game)
    except Exception as e:
        ventana.after(0, append_chat, f"Error al aceptar conexión: {e}\n")
        return

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                ventana.after(0, append_chat, "Conexión cerrada por el cliente\n")
                break

            mensaje = data.decode()
            ventana.after(0, append_chat, "Cliente: " + mensaje + "\n")
        except Exception as e:
            ventana.after(0, append_chat, f"Error al recibir: {e}\n")
            break

threading.Thread(target=aceptar, daemon=True).start()

# --------- ENVIAR MENSAJES ---------
def enviar(event=None):
    msg = entrada.get()

    if conn:
        try:
            conn.send(msg.encode())
        except Exception as e:
            ventana.after(0, append_chat, f"Error al enviar: {e}\n")
            return
    else:
        ventana.after(0, append_chat, "No hay conexión activa\n")
        return

    ventana.after(0, append_chat, "Tú: " + msg + "\n")
    entrada.delete(0, tk.END)

entrada.bind("<Return>", enviar)

boton = tk.Button(ventana, text="Enviar", command=enviar)
boton.pack()

# --------- EJECUTAR LA VENTANA ---------
if __name__ == "__main__":
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