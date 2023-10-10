import json
import time
#import random
#import math
import heapq
from collections import defaultdict

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

# Función para dividir un mensaje binario en paquetes de 8 bits
def dividir_en_paquetes(binario, longitud_paquete=8):
    paquetes = [binario[i:i+longitud_paquete] for i in range(0, len(binario), longitud_paquete)]
    return paquetes

def frecuencias_paquetes(paquetes):
    frecuencias = {paquete: paquetes.count(paquete) for paquete in paquetes}
    return frecuencias

def codificar_huffman(paquetes):
    frecuencias = frecuencias_paquetes(paquetes)
    # Crear una lista de nodos a partir de las frecuencias
    nodos = [[frecuencia, [simbolo, ""]] for simbolo, frecuencia in frecuencias.items()]
    
    # Convertir la lista en un montículo (heap)
    heapq.heapify(nodos)

    while len(nodos) > 1:
        # Tomar los dos nodos con las frecuencias más bajas
        izq = heapq.heappop(nodos)
        der = heapq.heappop(nodos)
        
        # Agregar "0" a los códigos de la izquierda y "1" a los de la derecha
        for nodo in izq[1:]:
            nodo[1] = '0' + nodo[1]
        for nodo in der[1:]:
            nodo[1] = '1' + nodo[1]

        # Crear un nuevo nodo combinando los dos nodos anteriores
        nuevo_nodo = [izq[0] + der[0]] + izq[1:] + der[1:]
        
        # Agregar el nuevo nodo al montículo
        heapq.heappush(nodos, nuevo_nodo)

    # El último nodo en el montículo es la raíz del árbol de Huffman
    arbol_huffman = sorted(heapq.heappop(nodos)[1:], key=lambda p: len(p[-1]))

    # Crear un diccionario de codificación
    codificacion = {}
    for simbolo, codigo in arbol_huffman:
        codificacion[simbolo] = codigo

    # Aplicar la codificación Huffman a los paquetes
    paquetes_codificados = [codificacion[paquete] for paquete in paquetes]

    return paquetes_codificados, codificacion

# Función para agregar un 1 al inicio del mensaje binario
def transmisor(binario):
    paquetes = dividir_en_paquetes(binario)  # Dividir el mensaje binario en paquetes de 8 bits

    # Aplica la codificación Huffman a los paquetes
    paquetes_codificados, codificacion_huffman = codificar_huffman(paquetes)

    mensaje_codificado = []
    for paquete_codificado in paquetes_codificados:
        mensaje_codificado.append('1' + paquete_codificado)  # Agregar "1" al inicio de cada paquete codificado
        
    return mensaje_codificado, codificacion_huffman

# Canal (sin ruido)
def canal(mensaje_transmitido, velocidad_transmision=1000):
    print("Iniciando transmisión a través del canal de cable coaxial.......")
    
    # Parámetros de simulación
    duracion_intervalo = 1 / velocidad_transmision  # Duración de cada intervalo de tiempo en segundos

    mensaje_recibido = []
    
    # Simular la transmisión de bit por bit
    for paquete in mensaje_transmitido:
        mensaje_recibido.append(paquete)
        time.sleep(duracion_intervalo)  
    
    #contar los paquetes transmitidos
    total_paquetes_transmitidos = len(mensaje_recibido)
    
    print("Transmisión completada.")
    print(f"Total de paquetes transmitidos: {total_paquetes_transmitidos}")
    
    return mensaje_recibido

# Funcion para decodificar huffman apartir de la tabla de huffman
def decodificar_huffman(mensaje_transmitido, codificacion_huffman):
    mensaje_decodificado = ''
    codigo_actual = ''
    
    for paquete in mensaje_transmitido:
        codigo_actual += paquete
        # Buscar si el código en el paquete coincide con el codigo huffman en el diccionario
        for simbolo, codigo in codificacion_huffman.items():
            if codigo_actual == codigo:
                mensaje_decodificado += simbolo # si encuentra la coincidencia agrega el simbolo del codigo a mensaje decodificado
                codigo_actual = ''  # se restablece el código actual para seguir buscando coincidencias
    
    return mensaje_decodificado

# Función para decodificar el mensaje y eliminar el primer 1, luego decodificar Huffman
def receptor(mensaje_transmitido, codificacion_huffman):
    print("Iniciando recepción y decodificación del mensaje...")
    mensaje_recibido = []

    for paquete_codificado in mensaje_transmitido:
        #print(f"Paquete codificado recibido: {paquete_codificado}")

        # Eliminar el primer "1" del inicio del paquete
        paquete_sin_uno = paquete_codificado[1:]

        # Decodificar el paquete usando la tabla de codificación Huffman
        paquete_decodificado = decodificar_huffman(paquete_sin_uno, codificacion_huffman)
        # Agregar el paquete decodificado al mensaje recibido
        mensaje_recibido.append(paquete_decodificado)

        # Imprimir el paquete decodificado
        #print(f"Paquete decodificado: {paquete_decodificado}")

    print("Recepción y decodificación completadas.")

    return mensaje_recibido

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
    print("\nfuente de información")
    datos_json_original = leer_json(ubicacion_json)  # Leer el JSON
    if datos_json_original is None:
        print("Error: No se pudo cargar el archivo JSON.")
    else:
        print("Datos JSON leídos (original):", datos_json_original)

    mensaje_binario = fuenteinfo(json.dumps(datos_json_original))

    # etapa del transmisor
    print("\ntransmisor")
    # Mostrar el mensaje binario antes de la codificación Huffman
    print("Mensaje binario (antes de la codificación Huffman):", mensaje_binario)
    # Transmitir el mensaje binario con codificación Huffman y "1" al inicio de cada paquete
    mensaje_transmitido, codificacion = transmisor(mensaje_binario)
    print("\nCodificación Huffman:")
    for simbolo, codigo in codificacion.items():
        print(f"{simbolo}: {codigo}")

    # etapa del canal
    print("\ncanal")
    mensaje_recibido = canal(mensaje_transmitido)
    # Imprimir el mensaje recibido
    print("Mensaje recibido:", mensaje_recibido)

    # etapa del receptor
    print("\nreceptor")
    mensaje_decodificado = receptor(mensaje_recibido, codificacion)
    # Convertir el mensaje decodificado en una cadena binaria completa
    mensaje_decodificado = ''.join(mensaje_decodificado)
    # Mostrar el mensaje binario recuperado
    print("Mensaje decodificado:")
    print(mensaje_decodificado)
        
    # destino de la información
    print("\ndestino de la información")
    # Convertir el mensaje binario en cadena JSON
    try:
        datos_recuperados = json.loads(binario_a_cadena(mensaje_decodificado))
        print("Datos JSON recuperados:")
        destinoinfo(datos_recuperados)
    except json.JSONDecodeError:
        # Mostrar la información sin convertirla en JSON
        print("\nInformación recuperada :")
        print(binario_a_cadena(mensaje_decodificado))
        print("El mensaje decodificado contiene un JSON inválido debido al ruido.")
if __name__ == "__main__":
    main()