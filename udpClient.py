import socket
import json
import time
import select

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

buf = properties['chunkSize']
timeout = 3
# envia mensaje al servidor
cliente.sendto('status OK'.encode(), serverAdr)

# booleano que determina se ya se termino de recivir el archivo
hay = True
# guarda el mensaje a medida que va llegando
mensajeTotal = ""

# Abre el archivo que va a guardar la informacion recibida
f = open('R_' + fileName, 'wb')

data, addr = cliente.recvfrom(buf)
while True:
    ready = select.select([cliente], [], [], timeout)
    if ready[0]:
        data, addr = cliente.recvfrom(buf)
        f.write(data)
    else:
        print ('Finish!' + fileName)
        f.close()
        break
