import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5000)
print('Conectando al bus en {}:{}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        continuar = input("¿Agendar una cita? (y/n): ")
        if continuar.lower() != 'y':
            break

        rut = input("RUT: ")
        fecha = input("Fecha (YYYY-MM-DD): ")
        hora = input("Hora (HH:MM): ")

        datos = f"{rut}|{fecha}|{hora}"
        mensaje = f"citax{datos}"
        mensaje_bytes = mensaje.encode()
        longitud = f"{len(mensaje_bytes):05}".encode()
        full_message = longitud + mensaje_bytes

        print("Enviando:", full_message)
        sock.sendall(full_message)

        print("Esperando respuesta...")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        data = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            if not chunk:
                break
            data += chunk
            amount_received += len(chunk)

        print("Respuesta recibida:", data.decode())

finally:
    print('Cerrando socket del cliente')
    sock.close()