import socket

def iniciar_servicio_cita():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 5000))
    try:
        # Registro del servicio en el bus
        mensaje_registro = b'00010sinitcita'
        sock.sendall(mensaje_registro)
        print("[CITA] Servicio de citas registrado.")

        while True:
            encabezado = sock.recv(5)
            if not encabezado:
                break
            longitud = int(encabezado.decode())
            mensaje = sock.recv(longitud).decode()
            print(f"[CITA] Mensaje recibido: {mensaje}")

            # Simulación de procesamiento
            respuesta_texto = f"[OK] Cita procesada: {mensaje}"
            respuesta_bytes = respuesta_texto.encode()
            longitud_respuesta = f"{len(respuesta_bytes):05}".encode()
            sock.sendall(longitud_respuesta + respuesta_bytes)

    except Exception as e:
        print(f"[!] Error en servicio_cita: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    iniciar_servicio_cita()