import socket
import json
import time

# Obtiene las propiedades del servidor del archivo configUDP.txt


def getProperties():
    with open('configUDP.txt', 'r') as file:
        properties = json.load(file)
    return properties


properties = getProperties()
# genera un socket UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# direccion del servidor
serverAdr = (properties['serverIp'], int(properties['serverPort']))

fileName = properties['fileName']
# envia mensaje al servidor
cliente.sendto('status OK'.encode(), serverAdr)

# booleano que determina se ya se termino de recivir el archivo
hay = True
# guarda el mensaje a medida que va llegando
mensajeTotal = ""
# contador de paquetes que recibe
i = 0
# Abre el archivo que va a guardar la información recibida
f = open('R_' + fileName, 'w')

# intensity of protocol messages
intensity = properties['intensity']

# timer para hacer timeout de la conexión
timer = time.time()
timeout = int(properties['timeout'])
# while para recibir y enviar mensajes
while hay:
        # envia mensaje al servidor
    message, addrSerer = cliente.recvfrom(1024)
    # recibe el mensaje y lo guarda en la
    if 'END_OF_FILE' not in message.decode():
        # se incrementa el numero de paquetes recibidos
        i = i + 1
        # se añade el mensaje que llego al que ya había
        mensajeTotal = mensajeTotal + message
        if i % 100 == 0:
            print("receiving data..")
    # Si el mensaje contiene "acabe" se cambia ha false la variable booleana y se incrementa el numero de paquetes
    else:
        # cambio de la variable
        hay = False
        # Incrementa el número de paquetes
        i = i + 1
        print('received END_OF_FILE')

    if (time.time() - timer) >= timeout:
        hay = False
# Escribe el archivo.
f.write(mensajeTotal)
# Cierra el archivo.
f.close()
# print(mensajeTotal)
# print (i)
for j in range(intensity):
    cliente.sendto(str(i).encode(), serverAdr)
