import socket
import threading
import model




class Server():
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        

    def start(self):
        self.sock.listen(1)
        print(f"Servidor escuchando en {self.host}:{self.port}")
        while True:
            conn, addr = self.sock.accept()
            print(f"Conexión establecida desde {addr}")
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        while True:
            self.db = model.Formulario()
            message = conn.recv(1024).decode('utf-8')
            if not message:
                break
            self.nombre, self.apellido, self.fecha = message.split(',')
            self.db.fecha = self.fecha
            self.db.nombre = self.nombre
            self.db.apellido = self.apellido
            self.db.save()
            conn.sendall(b"Datos recibidos correctamente")
            print(f"Mensaje recibido: Nombre: {self.nombre}, Apellido: {self.apellido}, Fecha: {self.fecha}")
        print(f"Conexión cerrada con {addr}")
        conn.close()


