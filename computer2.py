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
seed_proposal = None
remote_seed_proposal = None
agreed_seed = None
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


def process_command(message, source="local"):
    global seed_proposal, remote_seed_proposal, agreed_seed

    if message.startswith("/seed "):
        seed_value = message.split(" ", 1)[1].strip()
        if source == "local":
            seed_proposal = seed_value
            ventana.after(0, append_chat, f"Seed propuesto: {seed_value}\n")
        else:
            remote_seed_proposal = seed_value
            ventana.after(0, append_chat, f"Seed propuesto por servidor: {seed_value}\n")
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
                client.send(f"/start {agreed_seed}".encode())
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
                ventana.after(0, append_chat, "El servidor aceptó sin propuesta disponible.\n")
                return True
            launch_game(agreed_seed)
            ventana.after(0, append_chat, f"Servidor aceptó seed {agreed_seed}. Iniciando...\n")
            return True

    if message.startswith("/start "):
        seed_value = message.split(" ", 1)[1].strip()
        agreed_seed = seed_value
        launch_game(seed_value)
        ventana.after(0, append_chat, f"Juego iniciado por orden remota con seed: {seed_value}\n")
        return True

    return False


def recibir():
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                ventana.after(0, append_chat, "Conexión cerrada por el servidor\n")
                break

            mensaje = msg.decode()
            if not process_command(mensaje, source="remote"):
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


if connected_ok:
    ventana.after(0, append_chat, f"Conectado a servidor en {HOST}:{PORT}\n")
    show_local_ip()
    ventana.after(0, append_chat, "Use /seed <valor> para proponer seed, /agree para aceptar, o /start <valor> para iniciar.\n")
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

    if not process_command(msg, source="local"):
        chat.insert(tk.END, "Tú: " + msg + "\n")
    entrada.delete(0, tk.END)

entrada.bind("<Return>", enviar)

boton = tk.Button(ventana, text="Enviar", command=enviar)
boton.pack()

ventana.mainloop()

client.close()