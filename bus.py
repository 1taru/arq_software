import socket
import threading

# Diccionario para registrar servicios: {'cita': (conn, address), ...}
servicios_registrados = {}

def manejar_conexion(conn, addr):
    print(f"[+] Conexión recibida de {addr}")
    try:
        while True:
            encabezado = conn.recv(5)
            if not encabezado:
                break
            longitud = int(encabezado.decode())
            mensaje = conn.recv(longitud).decode()

            # Identificar tipo de mensaje
            if mensaje.startswith("sinit"):  # Registro de servicio
                nombre_servicio = mensaje[5:10]
                servicios_registrados[nombre_servicio] = conn
                print(f"[+] Servicio '{nombre_servicio}' registrado desde {addr}")
            else:
                nombre_servicio = mensaje[:5]
                contenido = mensaje[5:]
                print(f"[>] Reenviando a servicio '{nombre_servicio}' -> {contenido}")
                
                if nombre_servicio in servicios_registrados:
                    servicio_conn = servicios_registrados[nombre_servicio]
                    # Enviar mensaje al servicio
                    servicio_conn.sendall(encabezado + mensaje.encode())

                    # Esperar respuesta del servicio
                    respuesta_len = int(servicio_conn.recv(5).decode())
                    respuesta = servicio_conn.recv(respuesta_len)
                    # Reenviar al cliente
                    conn.sendall(f"{respuesta_len:05}".encode() + respuesta)
                else:
                    conn.sendall(b"00020ERROR: Servicio no existe")

    except Exception as e:
        print(f"[!] Error con {addr}: {e}")
    finally:
        conn.close()

def iniciar_bus():
    host = 'localhost'
    puerto = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, puerto))
    sock.listen()
    print(f"[BUS] Esperando conexiones en {host}:{puerto}...")

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=manejar_conexion, args=(conn, addr)).start()

if __name__ == "__main__":
    iniciar_bus()