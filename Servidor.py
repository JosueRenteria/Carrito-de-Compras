# Declaracion de librerias.
from socket import *
import sys

#--------------------------------------------------------------------------------------
# Funcion para Envia un Archivos.
def enviar_archivo(socket: socket, file_name, cliente_addres):
    # Declaracion del Buffer.
    buffer = 1024
    # Manejar el Archivo.
    f = open(file_name,"rb")
    data = f.read(buffer)

    # Enviar el archivo.
    socket.sendto(file_name.encode(), cliente_addres)
    socket.sendto(data, cliente_addres)

    # Proceso que envia el archivo en porciones.
    while (data):
        if(socket.sendto(data,cliente_addres)):
            print ("sending ...")
            data = f.read(buffer)
    
    # Cierre de nuestro archivo.
    f.close()
#--------------------------------------------------------------------------------------

# Dirreccion Loopback y puerto de Escucha.
direccion_servidor = "127.0.0.1"
puerto_servidor = 9099

# Creamos el servidor con el protocolo UDP
socket_servidor= socket(AF_INET, SOCK_DGRAM)

# Establecer la coneccion con el servidor.
socket_servidor.bind((direccion_servidor, puerto_servidor))

# Mensaje de Inicio.
print("El servidor esta listo para resivir.")

while True:
    # Resivimos que nuestro Cliente se Conecto.
    mensaje, cliente_addres = socket_servidor.recvfrom(4096)
    print('received {} bytes from {}'.format(len(mensaje), cliente_addres))
    mensaje_listo = mensaje.decode()

    # Para numeros (Con condiciones).
    match mensaje_listo:
        case  "1":
            # Nombre y ruta del archivo que se va a enviar.
            file_name="ListaServidor/Canciones.txt"
            # Llamamos a la funcion que Enviara el archivo.
            enviar_archivo(socket_servidor, file_name, cliente_addres)

        case _:
            print("Error")

    #socket_servidor.close()