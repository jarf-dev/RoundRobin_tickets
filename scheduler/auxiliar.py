from datetime import datetime
from base64 import b64encode

def timeLog(logMessage):
    logOutput= datetime.now().strftime("%d-%m-%Y %H:%M:%S") + \
        " : " + logMessage
    return print(logOutput)

# Función para codificar string a encode 64
def string2encode64(txtInput):
    return b64encode(txtInput.encode('ascii')).decode('ascii')