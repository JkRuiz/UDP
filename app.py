from flask import Flask, request, flash
import json


app = Flask(__name__)
numberClients = 0
indicator = 1
contador = 0


def get_indicator():
    global contador, numerClientes, indicator
    if contador < numberClients * 2:
        contador += 1
    else:
        indicator += 1
        contador = 1
    return indicator


def get_clients():
    with open('configTCP.json', 'r') as file:
        properties = json.load(file)
        clients = int(properties['numberClients'])
    return clients


@app.route('/metrics', methods=['POST'])
def register():
    reqJson = json.loads(request.json)
    indicator = get_indicator()
    fileName = 'Metrics/metrics_T' + str(indicator) + '.txt'
    with open((fileName), "a") as metrics:
        ip = str(reqJson['ipClient'])
        receivedBytes = str(reqJson['bytes'])
        time = str(reqJson['time'])
        metrics.write('Cliente - ' + ip + '\n')
        metrics.write('Bytes recibidos - ' + receivedBytes + '\n')
        metrics.write('Fecha - ' + time + '\n')
        metrics.write('--------------------------------------------------' + '\n')
    return('', 204)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    contador = 0
    numberClients = get_clients()
    app.run(host='192.168.10.3')
