# Declaracion de librerias.
from socket import *
from time import sleep
import sys
import re
import os
import copy

#--------------------------------------------------------------------------------------
# Funcion del encabezado de nuestro menu,
def Encabezado():
    print("\t\tBIENVENIDO AL CENTRO DE COMPRAS\n")
    print("\t1_Listar catalogo.")
    print("\t2_Agregar al Carrito.")
    print("\t3_Ver Carrito.")

    print("\t4_Finalizar Compra.\n")

# Funcion para saber si hay canciones repetidas.
def canciones_repetidas(canciones_usuario, canciones_compradas):
    no_canciones = 0
    print("\n")

    # Buscador de canciones repetidas.
    for i in canciones_usuario:
        for j in canciones_compradas:
            if(i==j):
                print(f"La cancion {i} ya se compro. Por favor eliminela.")
                no_canciones += 1
    print("\n")
    return no_canciones

# Funcion para Resivir un Archivos.
def resivir_archivo(file_name, socket: socket):
    # Declaracion del Buffer.
    buffer = 1024
    # Resivir el Nombre del Archivo. 
    data, servidor_addres = socket.recvfrom(buffer)

    # Abrimos y resivimos el archivo.
    print("Received File:",data.strip())
    f = open(file_name,"wb")
    # Resivimos los datos.
    data, servidor_addres = socket.recvfrom(buffer)

    # Funcion para resivir los metadatos del archivo.
    try:
        while(data):
            # Guardamos los Datos, escribimos el archivo creado.
            data, servidor_addres = socket.recvfrom(buffer)
            f.write(data)
            socket.settimeout(2)
    # Salida del proceso while.        
    except timeout:
        f.close()
    
    # Mensaje de que el Archivo se resivio.
    print ("Catalogo Resivido.")
    sleep(2)
    os.system('cls')

# Funcion que crea un archivo, de resivo.
def crear_archivo(canciones_usuario):
    # Este metodo crea y escribe en un archivo.
    with open("CancionesCompradas/CancionesCompradas.txt", "a") as archivo:
        for i in range(len(canciones_usuario)):

            # Si se corre 2 veces al final se escribe de nuevo el contenido.
            archivo.write(f"{canciones_usuario[i]}\n")

# Funcion para mostrar el catalogo.
def Catalogo():
    # Nombre del Archivo y Encabezados.
    print("\t\t####################")
    print("\t\t#LISTA DE CANCIONES#")
    print("\t\t####################\n")
    lista = ["Nombre de la Cancion: ","Autor: ","Genero: ","Tiempo: ", "Año: "]
    ruta_archivo = "ListaCliente/Canciones.txt"
    contador = 0

    # Abrimos el archivo que deseamos.
    with open(ruta_archivo) as archivo:
        # Aqui leemos el archivo y lo guaradamos.
        contenido = archivo.read()
        # Quitamos los espacios y comar para mostrar la Lista de las Canciones.
        lineas = re.split(",|\n",contenido)
    
    # Mostrar las opciones de Canciones que se Tienen.
    for i in range(len(lineas)): #  Len es para saber el tamaño de una lista.
        print("\t" + lista[contador]+ lineas[i])
        contador = contador + 1
        if contador == 5: 
            contador = 0
            print("\n")

# Funcion para Agregar al Carrito.
def Agregar_Carrito(canciones_usuario):
    salir = 0
    while (salir == 0):
        # Nombre del Archivo y Encabezados.
        print("\t\t###################")
        print("\t\t#AGREGAR CANCIONES#")
        print("\t\t###################\n")
        print("De las sigientes canciones agrega el nombre de las canciones que deseas o 0 para Salir.\n")
        lista = ["Nombre de la Cancion: ","Autor: ","Genero: ","Tiempo: ", "Año: "]
        ruta_archivo = "ListaCliente/Canciones.txt"
        contador = 0

        # Abrimos el archivo que deseamos.
        with open(ruta_archivo) as archivo:
            # Aqui leemos el archivo y lo guaradamos.
            contenido = archivo.read()
            # Quitamos los espacios y comar para mostrar la Lista de las Canciones.
            lineas = re.split(",|\n",contenido)

        # Mostrar las opciones de Canciones que se Tienen.
        for i in range(len(lineas)): #  Len es para saber el tamaño de una lista.
            print("\t" + lista[contador]+ lineas[i])
            contador = contador + 1

            # Mostrar el arreglo de lista las 5 veces correspondientes.
            if contador == 5: 
                contador = 0
                print("\n")
        
        # Agregar Canciones al Carrito.
        cancion = str(input("\nIngrese el nombre de la cancion:")).lower()

        # Para agregar una cancion que no esta en el carrito.
        if ((cancion in canciones_usuario) == False) and ((cancion in lineas) == True):
            canciones_usuario.append(cancion)
            print(f"\nLa cancion {cancion} se agrego correctamente al Carrito.")
            os.system('pause')
            os.system('cls')
        # Cuando una Cancion ya se agrego al Carrito.
        elif (cancion in canciones_usuario) == True:
            print(f"\nLa cancion {cancion} ya se agrego al carrito.")
            os.system('pause')
            os.system('cls')
        # Salir del apartado.
        elif cancion == "0":
            salir = 1
            return canciones_usuario
        # Cuando la cancion no se encuentra.
        else:
            print(f"\nLa cancion {cancion} no se encuentra. Revisalo por favor\n")
            os.system('pause')
            os.system('cls')

# Funcion para Borrar (canciones que ya se compraron) y Finalizar Compra.
def Compra(canciones_usuario, canciones_compradas):
    salir = 0 # Variable para salir.
    operacion = 0

    while salir == 0:
        # Variables solo para verificar lo que se esta haciendo.
        print(canciones_usuario)
        print(canciones_compradas)
        
        # Opcuion cuando tenemos informacion en el carrito de Compras.
        if (len(canciones_usuario) > 0):
            # Encabezados.
            print("\t\t##################")
            print("\t\t#FINALIZAR COMPRA#")
            print("\t\t##################\n")
            print("A continuacion se mostrara el nombre de las canciones que estan en el Carrito.\n")
            
            # Mostrar las canciones que tenemos en el Carrito
            for i in range(len(canciones_usuario)):
                print(f"\t{i+1}_{canciones_usuario[i]}")
            
            # Resivir informacion de entrada para ver que se desea hacer.
            print("\nSi quieres eliminar alguna cancion antes de pagar agrega el Nombre de la Cancion.")
            print("Si deseas Finalizar la compra pon Finalizar.\n")
            cancion = str(input("Agrega la opcion deseada:")).lower()

            # Cuando queremos eliminar una cancion del carrito.
            if ((cancion in canciones_usuario) == True) and ((cancion in canciones_compradas) == False):
                canciones_usuario.remove(cancion)
                print(f"La cancion {cancion} se elimino correctamente.")
                os.system('pause')
            
            # Cuando una cancion ya se compro previamente y queremos eliminar la cancion repetida.
            elif (cancion in canciones_compradas) == True:
                print(f"La cancion {cancion} ya se compro. Se eliminara.")
                canciones_usuario.remove(cancion)
                os.system('pause')
            
            # Para realizar la compra.
            elif cancion == "finalizar":
                # Llamamos a la funcion que verifica si no hay canciones ya compradas que se quieren comprar otra vez.
                no_canciones = canciones_repetidas(canciones_usuario, canciones_compradas)

                # Cuando ya no hay canciones repetidas y se quiere termionar la compra.
                if no_canciones == 0:
                    # Animados las canciones compradas por si ya teniamos antes compradas.
                    canciones_compradas.extend(canciones_usuario)

                    # Creamos un archivo de Resivo.
                    crear_archivo(canciones_usuario)
                    tamaño_envio = len(canciones_usuario)

                    # Borramos el carrito despues de crear nuestro Archivo.
                    os.system('pause')
                    salir = 1
                    operacion = 1
                else:
                    print("Por favor elimina las Canciones para poder finalizar la compra.\n")
                    os.system('pause')
            
            # Opcion para Salir.
            elif cancion == "0":
                salir = 1

            # Cuando se agrega algo erroneo.
            else:
                print("\nDato erroneo, por favor ingresar un Dato Correcto.")

        # Cuando no se agrego nada al Carrito.
        else:
            print("\nNo tienes ninguna cancion, por favor agrega alguna.")
            os.system('pause')
            salir = 1

        os.system('cls')
        
    return canciones_compradas, canciones_usuario, operacion
#--------------------------------------------------------------------------------------

# Dirreccion Loopback y puerto de Envio.
direccion_servidor = "127.0.0.1"
puerto_servidor = 9099
buffer = 1024

# Creamos el servidor con el protocolo UDP
socket_cliente = socket(AF_INET, SOCK_DGRAM)
cont = 0
# Canciones que tiene el usuario en su Carrito.
canciones_usuario = []
canciones_compradas = []

while cont == 0:
    # Mensaje de entrada.
    Encabezado()
    mensaje = input("Ingresa la opcion deseada:")

    # Enviamos la opcion deseada por el usuario.
    socket_cliente.sendto(mensaje.encode(),(direccion_servidor, puerto_servidor))

    # Para numeros (Con condiciones).
    match mensaje:
        # Ver el Catalogo de las Canciones.
        case  "1":
            # Nombre y ruta del archivo que se creara.
            file_name = "ListaCliente/Canciones.txt"

            # Mandamos a llamar a la funcion de resivir archivo y la que muestra el Catalogo.
            resivir_archivo(file_name, socket_cliente)
            Catalogo()

            # Borramos y Pausamos.
            os.system('pause')
            os.system('cls')
            
        case  "2":
            # Llamamos a la funcion Agregar al Carrito.
            canciones_usuario = Agregar_Carrito(canciones_usuario)
            os.system('cls')
            print(canciones_usuario) # Print solo para controlar que se hizo correctamente el proceso.

        case  "3":
            # Borramos y Pausamos.
            os.system('pause')
            os.system('cls')

            # Mandar a llamar la funcion de compra.
            canciones_compradas, canciones_usuario, operacion = Compra(canciones_usuario, canciones_compradas)

            # Condicion si se hizo correctamente el proceso.
            if operacion == 1:
                print(canciones_compradas)  # Print solo para controlar que se hizo correctamente el proceso.
                print(canciones_usuario)  # Print solo para controlar que se hizo correctamente el proceso.
                
                # Enviamos la opcion de resivir el resivo de compras.
                mensaje = "6"
                socket_cliente.sendto(mensaje.encode(),(direccion_servidor, puerto_servidor))
                
                # Enviar el tamaño del Arreglo.
                mensaje = str(len(canciones_usuario))
                print(mensaje)
                socket_cliente.sendto(mensaje.encode(),(direccion_servidor, puerto_servidor))

                # Aqui se envia el Arreglo.
                for i in range(len(canciones_usuario)):
                    mensaje = str(canciones_usuario[i])
                    socket_cliente.sendto(mensaje.encode(),(direccion_servidor, puerto_servidor))

                # Resivimos todas las canciones Compradas.
                for i in range(len(canciones_usuario)):
                    list = canciones_usuario[i]
                    print(list)
                    file_name = "CancionesCompradas/" + list + ".mp3"
                    print(file_name)
                    resivir_archivo(file_name, socket_cliente)
                
                #canciones_usuario.clear()

                # Borramos y Pausamos.
                os.system('pause')
                os.system('cls')

        case _:
            print("Saliendo")
            cont = 1

# Cierre de nuestro socket.
print("Socket Cerrado")
socket_cliente.close()