import socket
import re

class Client:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.host, self.port))
        print(f"Conectado al servidor en {self.host}:{self.port}")

    def send_messages(self):
        while True:
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            fecha = input("Ingrese la fecha(en formato DD/MM/YYYY): ")
            if not re.match(r'\d{2}/\d{2}/\d{4}$', fecha):
                print("Formato de fecha incorrecto. Debe ser DD/MM/YYYY")
                continue
            message = f"{nombre},{apellido},{fecha}"
            self.sock.sendall(message.encode('utf-8'))
            response = self.sock.recv(1024)
            print(f"Respuesta del servidor: {response.decode('utf-8')}")

if __name__ == '__main__':
    client = Client()
    client.connect()
    client.send_messages()
