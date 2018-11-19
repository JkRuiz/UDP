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


def threaded_function(id, addr):
    timmer = datetime.datetime.now()
    # print(id)
    start = datetime.datetime.now()
    # contador de paquetes
    i = 0

    # booleano para saber hasta cuando debe seguir activo el while.
    hay = True

    rsp = "Sending " + fileName

    sout("S: " + rsp + " to C" + str(id) + " with IP " + addr[0] + " and port " + str(addr[1]))

    # recepción y envio de mensajes.
    while hay:
        start = datetime.datetime.now()

        for chunk in fileChunks:
            serverSocket.sendto(chunk, addr)
            i = i + 1

        sout("S: END_OF_FILE")

        # envia mensaje para que el cliente sepa que se termino la transmicion.
        outputData = 'END_OF_FILE'

        # imprime el mensaje de terminar.
        # print(outputData)

        # aumenta el contador de paquetes.
        i = i + 1

        # envia el mensaje de termino.
        for i in range(intensity):
            serverSocket.sendto(outputData.encode(), addr)

        # imprime el contador de mensajes.
        #print (i)

        sout("S: Se enviaron: " + str(i) + "paquetes")

        llego = False
        while (not llego):

            # recive el numero de pauqetes recibidos.
            data, addr = serverSocket.recvfrom(1024)
            if (data != ""):
                llego = True
                sout("S: Se recibieron: " + data.decode() + "paquetes")

        # imprime el numero de paquetes enviados.
        # print(data.decode())

        # indica la terminación del while.
        hay = False

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

# Tamaño de los paquetes que se van a usar.
chunkSize = int(properties['chunkSize'])

# Genera el log de la transacción.
logPrefix = properties['logPrefix'] + str(numeroClientes) + "_" + str(time.time()) + ".log"


# genera un socket UDP.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Obtiene el hostname sobre el que se ejecuta el programa.
host = socket.gethostname()

# la dirección y el puerto por donde el servidor va a escuchar.
serverSocket.bind(('', port))

# intensity of protocol messages
intensity = properties['intensity']


# load file to memory
fileChunks = []
with open(fileName, 'r') as f:
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
        # recibe los datos del socket y la dirección del cliente.
        data, addr = serverSocket.recvfrom(1024)
        if 'status OK' in data.decode():
            sout("C" + str(j) + ": " + data.decode())
            #print (data.decode())
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
