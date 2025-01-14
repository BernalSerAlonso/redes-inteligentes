import socket

# Configuración del servidor
HOST = '178.28.96.240'  # Dirección del servidor (localhost o IP del laboratorio 1)
PORT = 5060         # Puerto típico para SIP
# Creación del socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print("Servidor SIP iniciado en {}:{}".format(HOST, PORT))
while True:
    data, addr = server_socket.recvfrom(1024)  # Recibe mensajes
    print(f"Mensaje recibido de {addr}: {data.decode()}")
    # Responde al cliente
    if "INVITE" in data.decode():
        response = "SIP/2.0 200 OK"
        server_socket.sendto(response.encode(), addr)
