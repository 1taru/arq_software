import socket

# Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5050)
print('Conectando al bus en {}:{}'.format(*bus_address))
sock.connect(bus_address)

try:
    # Enviar registro del servicio
    mensaje_registro = b'00010sinitreportes'
    print('Enviando registro: {!r}'.format(mensaje_registro))
    sock.sendall(mensaje_registro)
    sinit = True

    while True:
        print("Esperando transacción...")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        data = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            if not chunk:
                break
            data += chunk
            amount_received += len(chunk)

        print("Procesando mensaje recibido...")
        print("Mensaje crudo:", data)

        if sinit:
            print("Registro recibido.")
            sinit = False
            continue

        datos = data[5:].decode()
        partes = datos.split("|")
        if len(partes) == 2:
            tipo_reporte, fecha = partes
            respuesta = f"reportesOKReporte generado para {tipo_reporte} el {fecha}"
        else:
            respuesta = "reportesNKFormato inválido"

        respuesta_bytes = respuesta.encode()
        mensaje_respuesta = f"{len(respuesta_bytes):05}".encode() + respuesta_bytes
        print("Enviando respuesta:", mensaje_respuesta)
        sock.sendall(mensaje_respuesta)

finally:
    print('Cerrando socket del servicio')
    sock.close()