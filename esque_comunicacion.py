import json
import time

# Función para leer un JSON desde una ubicación
def leer_json(ubicacion):
    with open(ubicacion, 'r') as file:
        data = json.load(file)
    return data

# Función para convertir una cadena en binario
def fuenteinfo(cadena):
    binario = ''.join(format(ord(char), '08b') for char in cadena)
    return binario

# Función para agregar un 1 al inicio del mensaje binario
def transmisor(binario):
    mensaje_codificado = '1' + binario
    return mensaje_codificado

# Función para simular el canal de comunicación con retraso
def canal (mensaje_codificado):
    print("Enviando mensaje a través del canal...")
    time.sleep(3)  # Simulando el retraso de 3 segundos en el canal
    return mensaje_codificado

# Función para decodificar el mensaje y eliminar el primer 1
def receptor (mensaje_codificado):
    mensaje_decodificado = mensaje_codificado[1:]
    return mensaje_decodificado

# Función para convertir un mensaje binario a una cadena
def binario_a_cadena(binario):
    cadena = ''.join(chr(int(binario[i:i+8], 2)) for i in range(0, len(binario), 8))
    return cadena

# Función para visualizar los datos obtenidos del JSON
def destinoinfo(datos):
    print("Datos obtenidos:")
    print(datos)

# Ubicación del archivo JSON
ubicacion_json = '/Users/macbookair/Downloads/surf_report.json'

# Etapa de la fuente de información
datos_json = leer_json(ubicacion_json)
print("Datos JSON leídos:", datos_json)

# Etapa del transmisor
mensaje_binario = fuenteinfo(json.dumps(datos_json))
mensaje_codificado = transmisor(mensaje_binario)

# Etapa del canal
mensaje_enviado = canal (mensaje_codificado)
print("Mensaje recibido del canal:", mensaje_enviado)

# Etapa del receptor
mensaje_decodificado = receptor (mensaje_enviado)
datos_recuperados = json.loads(binario_a_cadena(mensaje_decodificado))
print("Datos JSON recuperados:", datos_recuperados)

# Etapa del destino de información
destinoinfo(datos_recuperados)