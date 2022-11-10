#encoding: utf-8

# Declaracion de librerias.
from time import sleep
from socket import *
import sys
import os
import re

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

def Mostrar_resivo(nombre):
    # Abrimos el archivo que deseamos.
    with open(nombre) as archivo:
        # Aqui leemos el archivo y lo guaradamos.
        contenido = archivo.read()
        # Quitamos los espacios y comar para mostrar la Lista de las Canciones.
        lista = re.split(",|\n",contenido)
    
    return lista
#--------------------------------------------------------------------------------------

# Dirreccion Loopback y puerto de Escucha.
direccion_servidor = "127.0.0.1"
puerto_servidor = 9099
buffer = 1024

# Creamos el servidor con el protocolo UDP
socket_servidor= socket(AF_INET, SOCK_DGRAM)

# Establecer la coneccion con el servidor.
socket_servidor.bind((direccion_servidor, puerto_servidor))

# Mensaje de Inicio.
print("El servidor esta listo para resivir.")

while True:
    lista = []
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
        
        case "6":
            # Resivimos el archivo.ddd
            print(f"El servidor resivira los elementos comprados por {cliente_addres}")

            #Resivir el Tamaño de la lista del Archivo.
            mensaje, cliente_addres = socket_servidor.recvfrom(4096)
            dato = int(mensaje.decode())
            print('received {} bytes from {}'.format(len(mensaje), cliente_addres))
            print(dato)

            # Aqui se envia el Arreglo.
            for i in range(dato):
                mensaje, cliente_addres = socket_servidor.recvfrom(4096)
                dato = str(mensaje.decode())
                print(dato)
                lista.append(dato)
            
            print(lista)

            # Aqui se envia todas las canciones.
            for i in range(len(lista)):
                list = lista[i]
                print(list)
                file_name = "Canciones(Servidor)/" + list + ".mp3"
                print(file_name)
                enviar_archivo(socket_servidor, file_name, cliente_addres)
            
            print("\nSe enviaron todas las canciones")

        case _:
            print("\nEsta en una opcion que no necesita el Servidor.\n")

    #socket_servidor.close()