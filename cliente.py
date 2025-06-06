import socket

# Función para conectar al bus
def conectar_al_bus():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5050)  # Asegúrate de que el puerto sea el correcto
    print('Conectando al bus en {}:{}'.format(*bus_address))
    sock.connect(bus_address)
    return sock

# Función para enviar mensajes al bus
def enviar_mensaje(sock, servicio, datos):
    mensaje = f"{servicio}{datos}"
    mensaje_bytes = mensaje.encode()
    longitud = f"{len(mensaje_bytes):05}".encode()
    full_message = longitud + mensaje_bytes

    print(f"[CLIENTE] Enviando mensaje: {full_message}")
    sock.sendall(full_message)

    print("[CLIENTE] Esperando respuesta...")
    amount_received = 0
    amount_expected = int(sock.recv(5))

    data = b''
    while amount_received < amount_expected:
        chunk = sock.recv(amount_expected - amount_received)
        if not chunk:
            break
        data += chunk
        amount_received += len(chunk)

    return data.decode()

# Función para agendar cita
def agendar_cita(sock):
    rut = input("RUT: ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    hora = input("Hora (HH:MM): ")

    datos = f"{rut}|{fecha}|{hora}"
    respuesta = enviar_mensaje(sock, "citax", datos)
    print("Respuesta recibida:", respuesta)

# Función para registrar usuario
def registrar_usuario(sock):
    nombre = input("Nombre: ")
    email = input("Email: ")
    telefono = input("Teléfono: ")

    datos = f"{nombre}|{email}|{telefono}"
    respuesta = enviar_mensaje(sock, "usuario", datos)
    print("Respuesta recibida:", respuesta)

# Función para generar reportes
def generar_reporte(sock):
    tipo_reporte = input("Tipo de reporte: ")
    fecha = input("Fecha (YYYY-MM-DD): ")

    datos = f"{tipo_reporte}|{fecha}"
    respuesta = enviar_mensaje(sock, "reportes", datos)
    print("Respuesta recibida:", respuesta)

# Función del menú para seleccionar la acción
def menu():
    print("Seleccione una opción:")
    print("1. Agendar una cita")
    print("2. Registrar usuario")
    print("3. Generar reporte")
    print("4. Salir")
    return input("Opción: ")

# Función principal para ejecutar el cliente
def main():
    sock = conectar_al_bus()

    try:
        while True:
            opcion = menu()

            if opcion == '1':
                agendar_cita(sock)
            elif opcion == '2':
                registrar_usuario(sock)
            elif opcion == '3':
                generar_reporte(sock)
            elif opcion == '4':
                break
            else:
                print("Opción inválida, intente de nuevo.")

    finally:
        print('Cerrando socket del cliente')
        sock.close()

if __name__ == "__main__":
    main()