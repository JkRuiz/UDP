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

# Abre el archivo que va a guardar la informacion recibida
f = open('R_' + fileName, 'wb')

# intensity of protocol messages
intensity = properties['intensity']

# timer para hacer timeout de la conexion
timer = time.time()
timeout = int(properties['timeout'])
# while para recibir y enviar mensajes
while hay:

    message, addrSerer = cliente.recvfrom(1024)

    try:
        if 'END_OF_FILE' not in message.decode():
            hay = False
            print('received END_OF_FILE')
    except:
        # se incrementa el numero de paquetes recibidos
        if i % 100 == 0:
            print("receiving data..")
        f.write(message)
    print('tiempo actual: ' + str(time.time() - timer))
    if (time.time() - timer) >= timeout:
        print('Se cumplio el timeout')
        hay = False

f.close()
cliente.close()
