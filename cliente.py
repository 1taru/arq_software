import socket

def enviar_mensaje_al_bus(servicio, contenido):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 5000))
    try:
        mensaje = f"{servicio}{contenido}"
        mensaje_codificado = mensaje.encode()
        longitud = f"{len(mensaje_codificado):05}".encode()
        print(f"[CLIENTE] Enviando mensaje: {mensaje}")
        sock.sendall(longitud + mensaje_codificado)

        # Recibir respuesta
        encabezado = sock.recv(5)
        longitud_respuesta = int(encabezado.decode())
        respuesta = sock.recv(longitud_respuesta).decode()
        print(f"[CLIENTE] Respuesta del servicio: {respuesta}")
    finally:
        sock.close()

if __name__ == "__main__":
    while True:
        contenido = input("Ingrese contenido de cita (ej: AGENDAR|RUT123|10-06|10:00): ")
        if contenido.lower() == "salir":
            break
        enviar_mensaje_al_bus("cita", contenido)