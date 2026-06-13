import socket

HOST = "192.168.1.34"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

while True:

    number = int(input("请输入数字: "))

    result = number * 2

    print("乘2结果:", result)

    client.send(str(number).encode())