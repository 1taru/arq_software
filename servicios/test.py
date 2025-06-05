import socket
s = socket.socket()
s.connect(('localhost', 5000))
print("Conexión exitosa con el bus")