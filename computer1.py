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
seed_proposal = None
remote_seed_proposal = None
agreed_seed = None
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


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip.startswith("127."):
            return None
        return ip
    except Exception:
        return None


def show_local_ip():
    ip_local = get_local_ip()
    if ip_local:
        ventana.after(0, append_chat, f"IP local de este equipo: {ip_local}\n")
    else:
        ventana.after(0, append_chat, "No se pudo determinar la IP local. Usa 'ipconfig' en CMD para ver la IP de este ordenador.\n")


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


def process_command(message, source="local"):
    global seed_proposal, remote_seed_proposal, agreed_seed

    if message.startswith("/seed "):
        seed_value = message.split(" ", 1)[1].strip()
        if source == "local":
            seed_proposal = seed_value
            ventana.after(0, append_chat, f"Seed propuesto: {seed_value}\n")
        else:
            remote_seed_proposal = seed_value
            ventana.after(0, append_chat, f"Seed propuesto por cliente: {seed_value}\n")
        return True

    if message == "/agree":
        if source == "local":
            if remote_seed_proposal:
                agreed_seed = remote_seed_proposal
            elif seed_proposal:
                agreed_seed = seed_proposal
            else:
                ventana.after(0, append_chat, "No hay seed propuesta para aceptar.\n")
                return True
            try:
                conn.send(f"/start {agreed_seed}".encode())
            except Exception:
                pass
            launch_game(agreed_seed)
            return True
        else:
            if seed_proposal:
                agreed_seed = seed_proposal
            elif remote_seed_proposal:
                agreed_seed = remote_seed_proposal
            else:
                ventana.after(0, append_chat, "El cliente aceptó sin propuesta disponible.\n")
                return True
            launch_game(agreed_seed)
            ventana.after(0, append_chat, f"Cliente aceptó seed {agreed_seed}. Iniciando...\n")
            return True

    if message.startswith("/start "):
        seed_value = message.split(" ", 1)[1].strip()
        agreed_seed = seed_value
        launch_game(seed_value)
        ventana.after(0, append_chat, f"Juego iniciado por orden remota con seed: {seed_value}\n")
        return True

    return False


def aceptar():
    global conn

    ventana.after(0, append_chat, "Esperando cliente en {}:{}...\n".format(HOST, PORT))
    show_local_ip()
    try:
        conn, addr = server.accept()
        ventana.after(0, append_chat, f"Cliente conectado: {addr}\n")
        ventana.after(0, append_chat, "Use /seed <valor> para proponer seed, /agree para aceptar, o /start <valor> para iniciar.\n")
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
            if not process_command(mensaje, source="remote"):
                ventana.after(0, append_chat, "Cliente: " + mensaje + "\n")
        except Exception as e:
            ventana.after(0, append_chat, f"Error al recibir: {e}\n")
            break

threading.Thread(target=aceptar, daemon=True).start()

# --------- ENVIAR MENSAJES ---------
def enviar(event=None):
    msg = entrada.get()

    if not process_command(msg, source="local"):
        if conn:
            try:
                conn.send(msg.encode())
            except Exception as e:
                ventana.after(0, append_chat, f"Error al enviar: {e}\n")
                return
            ventana.after(0, append_chat, "Tú: " + msg + "\n")
        else:
            ventana.after(0, append_chat, "No hay conexión activa\n")
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