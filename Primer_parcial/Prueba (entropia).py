import json
import time
import random
import math

# Función para leer un JSON desde una ubicación
def leer_json(ubicacion):
    try:
        with open(ubicacion, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"El archivo JSON en la ubicación {ubicacion} no se encontró.")
        return None
    except json.JSONDecodeError:
        print(f"El archivo JSON en la ubicación {ubicacion} no es válido.")
        return None

# Función para convertir una cadena en binario
def fuenteinfo(cadena):
    binario = ''.join(format(ord(char), '08b') for char in cadena)
    return binario

# Función para agregar un 1 al inicio del mensaje binario
def transmisor(binario):
    mensaje_codificado = '1' + binario
    return mensaje_codificado

# Función para simular el canal de comunicación con retraso aleatorio y ruido
def canal(mensaje_codificado):
    print("Iniciando transmisión a través del canal de cable coaxial....")

    # Parámetros de simulación
    retraso_minimo = 2  # Retraso mínimo en segundos
    retraso_maximo = 8  # Retraso máximo en segundos
    
    # Generar un retraso aleatorio dentro del rango especificado
    retraso_transmision = random.uniform(retraso_minimo, retraso_maximo)

    # Definir los números que introducirán retraso y ruido
    numeros_con_retraso = [13, 15, 17, 21, 23, 25, 31, 33, 35, 39]
    
    # Generar un número aleatorio entre 1 y 50
    numero_aleatorio = random.randint(1, 50)
    
    # Verificar si el número aleatorio está en la lista de números con retraso
    if numero_aleatorio in numeros_con_retraso:
        print("Ruido de retraso en la transmisión.")
        time.sleep(retraso_transmision)

        # Calcular la probabilidad de que ocurra el evento (retraso y ruido)
        probabilidad_evento = 1/10

        # Calcular la entropía debido al retraso y ruido en el canal
        entropia = -probabilidad_evento * math.log2(probabilidad_evento)
    
        # Mostrar el retraso total
        print(f"Retraso total en la transmisión: {retraso_transmision:.2f} segundos")
    else:
        entropia = 0  # Si no hay retraso ni ruido, la entropía es cero
    
    # Devolver el mensaje recibido y la entropía
    return mensaje_codificado, entropia

# Función para decodificar el mensaje y eliminar el primer 1
def receptor(mensaje_codificado):
    print("Iniciando recepción y decodificación del mensaje...")
    print(f"Mensaje codificado recibido: {mensaje_codificado}")
    
    mensaje_decodificado = mensaje_codificado[1:]
    
    print(f"Mensaje decodificado: {mensaje_decodificado}")
    print("Recepción y decodificación completadas.")
    
    return mensaje_decodificado

# Función para convertir un mensaje binario a una cadena
def binario_a_cadena(binario):
    cadena = ''.join(chr(int(binario[i:i+8], 2)) for i in range(0, len(binario), 8))
    return cadena

# Función para visualizar los datos obtenidos del JSON
def destinoinfo(datos):
    print("Datos obtenidos:")
    print(json.dumps(datos, indent=4))

def main():
    # Ubicación del archivo JSON (modificar de acuerdo a la ubicación del json)
    ubicacion_json = '/Users/macbookair/Downloads/surf_report.json'

    # fuente de información
    datos_json = leer_json(ubicacion_json)
    if datos_json is None:
        return

    print("Datos JSON leídos:", datos_json)

    # transmisor
    mensaje_binario = fuenteinfo(json.dumps(datos_json))
    mensaje_codificado = transmisor(mensaje_binario)

    # canal
    mensaje_recibido, entropia = canal(mensaje_codificado)  # Llamamos a la función y almacenamos el mensaje recibido

    # receptor
    mensaje_decodificado = receptor(mensaje_recibido)
    
    # Verificar si el mensaje decodificado no está vacío antes de intentar decodificarlo en JSON
    if mensaje_decodificado:
        try:
            datos_recuperados = json.loads(binario_a_cadena(mensaje_decodificado))
            print("Datos JSON recuperados:")
            destinoinfo(datos_recuperados)
        except json.JSONDecodeError:
            print("El mensaje decodificado contiene un JSON inválido debido a las modificaciones.")
    else:
        print("El mensaje decodificado está vacío o dañado.")
    print(f"Entropía debida al retraso y ruido en el canal: {entropia:.2f}")

if __name__ == "__main__":
    main()