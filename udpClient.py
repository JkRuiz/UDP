import socket
import json
import time
import select
import request as rq
import os

# Obtiene las propiedades del servidor del archivo configUDP.txt


def getProperties():
    with open('configUDP.txt', 'r') as file:
        properties = json.load(file)
    return properties


# Envia el numero de bytes recibidos antes de recibir el archivo
while(True):
    try:
        # connect to server, send as fileSize zero because theres no file yet
        rq.send_metric(0)
        break
    except:
        print('waiting for server to send metrics...')
        time.sleep(5)

# Eliminar el archivo si ya existe
    try:
        os.remove("R_" + fileName)
    except:
        print('The file didnt exist before')
        pass

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
        print ('Finish ' + fileName)
        f.close()
        break

fileSize = os.stat('R_' + fileName).st_size
rq.send_metric(fileSize)
