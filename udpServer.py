import socket
import json
import time
import datetime
from threading import Thread

# Obtiene las propiedades del servidor del archivo configUDP.txt


def getProperties():
    with open('configUDP.txt', 'r') as file:
        properties = json.load(file)
    return properties


def sout(l):
    log.write(l + '\n')
    log.flush()
    print(l)


def swapProperties():
    with open('configUDP.txt', 'r') as file:
        tmp = json.load(file)
        tmp['indicatorTest'] = tmp['indicatorTest'] + 1
    with open('configUDP.txt', 'w') as file:
        file.write(json.dumps(tmp))


def threaded_function(id, addr):

    start = datetime.datetime.now()

    rsp = "Sending " + fileName

    sout("S: " + rsp + " to C" + str(id) + " with IP " + addr[0] + " and port " + str(addr[1]))

    chunkIndex = 0
    data = fileChunks[chunkIndex]
    while (data):
        serverSocket.sendto(data, addr)
        if chunkIndex % 10000 == 0:
            print ('sending ...')
        chunkIndex += 1
        if chunkIndex < len(fileChunks):
            data = fileChunks[chunkIndex]
        else:
            data = None

    summary = str(datetime.datetime.now() - start) + "s"
    sout("C" + str(id) + ": Transfered in " + summary)


# Obtiene las propiesdades.
properties = getProperties()

# Nombre del archivo que se va a enviar.
fileName = properties['fileName']

# Numero de clientes a los que se escuchara.
numeroClientes = int(properties['numberClients'])

# Numero de puerto que se utilizara.
port = int(properties['serverPort'])

# Tamanio de los paquetes que se van a usar.
chunkSize = int(properties['chunkSize'])

indicatorTest = int(properties['indicatorTest'])
# Genera el log de la transaccion.
logPrefix = properties['logPrefix'] + str(indicatorTest) + "_Server.log"


# genera un socket UDP.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Obtiene el hostname sobre el que se ejecuta el programa.
host = socket.gethostname()

# la direccion y el puerto por donde el servidor va a escuchar.
serverSocket.bind(('', port))

# load file to memory
fileChunks = []
with open(fileName, 'rb') as f:
    l = f.read(chunkSize)
    while (l):
        fileChunks.append(l)
        l = f.read(chunkSize)

# abre el archivo del log y registra la hora y la fecha
with open((logPrefix), 'w') as log:

    sout('Server listening....')
    tStart = datetime.datetime.now()

    # arreglo de threads
    threads = []

    # Contador de clientes
    j = 1

    # Se crean los threads a medida que llegan clientes
    while j <= numeroClientes:
        # recibe los datos del socket y la direccion del cliente.
        data, addr = serverSocket.recvfrom(1024)
        if 'status OK' in data.decode():
            if j == 1:
                tStart = datetime.datetime.now()
            sout("C" + str(j) + ": " + data.decode())
            # print (data.decode())
            sout('Server adopted connection #' + str(j))
            if (data):
                thread = Thread(target=threaded_function, args=(j, addr))
                thread.start()
                threads.append(thread)
                j = j + 1

    # for que sincroniza los threads.
    for i in range(len(threads)):
        threads[i].join()

    summary = str(datetime.datetime.now() - tStart) + "s"
    sout("S: Transfered in " + summary)
    serverSocket.close()
    swapProperties()
