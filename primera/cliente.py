import socket

# Configuración del cliente
SERVER_HOST = '178.28.96.240' # Dirección del servidor SIP (IP del laboratorio 1)
SERVER_PORT = 5060
# Creación del socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Construcción de un mensaje INVITE
invite_message = "INVITE sip:user2@172.28.107.182 SIP/2.0\r\n"
client_socket.sendto(invite_message.encode(), (SERVER_HOST, SERVER_PORT))
print(f"Mensaje enviado al servidor: {invite_message}")
# Espera la respuesta
response, _ = client_socket.recvfrom(1024)
print(f"Respuesta del servidor: {response.decode()}")
