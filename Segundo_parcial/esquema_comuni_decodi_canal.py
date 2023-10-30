import json
import time
import random
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

def codificar_shannon(paquetes):
    # Obtener frecuencias y ordenar símbolos
    frecuencias = frecuencias_paquetes(paquetes)
    simbolos_ordenados = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)

    def crear_codigos(simbolos, codigo_actual, tabla):
        if len(simbolos) == 1:
            tabla[simbolos[0][0]] = codigo_actual
        else:
            mitad = len(simbolos) // 2
            crear_codigos(simbolos[:mitad], codigo_actual + '0', tabla)
            crear_codigos(simbolos[mitad:], codigo_actual + '1', tabla)

    # Llamar a la función recursiva para crear la tabla de códigos
    tabla_shannon = {}
    crear_codigos(simbolos_ordenados, '', tabla_shannon)

    # Aplicar la codificación Shannon-Fano a los paquetes
    paquetes_shannon = [tabla_shannon[paquete] for paquete in paquetes]

    return paquetes_shannon, tabla_shannon

def codificar_agregardiez(paquetes_binarios):
    paquetes_codificados = []

    for paquete_binario in paquetes_binarios:
        numero_decimal = int(paquete_binario, 2)
        numero_decimal += 10
        paquete_binario_codificado = format(numero_decimal, '08b')
        paquetes_codificados.append(paquete_binario_codificado)

    return paquetes_codificados

def codificar_gray(paquetes):
    paquetes_gray = []

    for binario in paquetes:
        gray = binario[0]
        for i in range(1, len(binario)):
            bit_gray = str(int(binario[i]) ^ int(binario[i - 1]))
            gray += bit_gray
        paquetes_gray.append(gray)

    return paquetes_gray

def handshake(eleccion, paquetes):
  # permitira proporcionar los diccionarios en caso de que la codificacion lo requiera para su decodificacion
    if eleccion == 's':
        paquetes_codificados, diccionario = codificar_shannon(paquetes)
        codificacion_utilizada = "Shannon-Fano"
    elif eleccion == 'h':
        paquetes_codificados, diccionario = codificar_huffman(paquetes)
        codificacion_utilizada = "Huffman"
    elif eleccion == 'd':
        paquetes_codificados = codificar_agregardiez(paquetes)
        diccionario = None  # no necesita un diccionario para Sumadiez
        codificacion_utilizada = "Suma Diez"
    elif eleccion == 'g':
        paquetes_codificados = codificar_gray(paquetes)
        diccionario = None  # no necesita un diccionario para Gray
        codificacion_utilizada = "Código Gray"
    else:
        print("No se selecciono ninguna codificacion valida. No se aplicara Codificación a los paquetes.")
        paquetes_codificados = paquetes
        diccionario = None  # No se necesita un diccionario
        codificacion_utilizada = "Sin codificación"

    return paquetes_codificados, diccionario, codificacion_utilizada

# transmisor
def transmisor_d(binario):
    # Saber qué codificación se usará
    eleccion = input("¿Desea utilizar codificación Shannon-Fano (S), Huffman (H), Sumar Diez (D) o Código Gray (G)? ").strip().lower()

    paquetes = dividir_en_paquetes(binario)  # Se divide el binario en paquetes de 8 bits

    # Llama a handshake con la elección del usuario
    mensaje_codificado, diccionario, codificacion_utilizada = handshake(eleccion, paquetes)

    mensaje = []  # para almacenar los paquetes

    for paquete_codificado in mensaje_codificado:
        mensaje.append('1' + paquete_codificado)  # Agregar "1" al inicio de cada paquete codificado

    return mensaje, diccionario, codificacion_utilizada

# Canal (sin ruido)
def canal_adaptativo(canales, paquetes):
    mensaje_recibido = []  # mensaje recibido
    canal_actual = 0  # indice del canal activo

    paquetes_transmitidos = []  # lista para los paquetes transmitidos

    for paquete in paquetes:
        while True:
            canal_activo = canales[canal_actual]  # Usar el canal actual
            print(f"Transmitiendo en {canal_activo['nombre']}: {paquete}")

            mensaje_recibido.extend(list(paquete))

            # probabilidad de perder el paquete: 30%
            if random.random() < 0.3:
                print("Se perdio el paquete. Cambiando al siguiente canal...")
                canal_actual = (canal_actual + 1) % len(canales) # cambiamos al siguiente canal
            else:
                paquetes_transmitidos.append(paquete)  # agregar el paquete a la lista 
                break  # romper el bucle

            time.sleep(1 / canal_activo['velocidad'])  # tiempo de transmisión

    return paquetes_transmitidos

def decodificar(mensaje_transmitido, codificacion):
    mensaje_decodificado = ''
    codigo_actual = ''
    
    for paquete in mensaje_transmitido:
        codigo_actual += paquete
        # Buscar si el código actual coincide con alguna clave de codificación
        for simbolo, codigo in codificacion.items():
            if codigo_actual == codigo:
                mensaje_decodificado += simbolo
                codigo_actual = ''  # Restablecer el código actual
                break  # Salir del bucle una vez que se ha encontrado la coincidencia

    return mensaje_decodificado

def decodificar_sumar_diez(paquete_codificado):

    numero_decimal = int(paquete_codificado, 2)
    numero_decimal -= 10
    paquete_binario_decodificado = format(numero_decimal, '08b')
    
    return paquete_binario_decodificado

def decodificar_gray(paquete_codificado):
    binario = ''
    for i in range(len(paquete_codificado)):
        bit_binario = str(int(paquete_codificado[i]) ^ int(binario[i - 1] if i > 0 else '0'))
        binario += bit_binario
    return binario

# receptor
# Función para decodificar el mensaje y eliminar el primer 1, luego decodificar Huffman
def receptor(mensaje_transmitido, diccionario, codificacion_utilizada):
    print("Iniciando recepción y decodificación del mensaje...")
    mensaje_recibido = []

    for paquete_codificado in mensaje_transmitido:
        # eliminar el primer "1" del inicio del paquete que se agrega en transmisor
        paquete_sin_uno = paquete_codificado[1:]

        # decodificar de acuerdo a la codificación utilizada
        if codificacion_utilizada == "Huffman" or codificacion_utilizada == "Shannon-Fano":
            paquete_decodificado = decodificar(paquete_sin_uno, diccionario)
        elif codificacion_utilizada == "Suma Diez":
            paquete_decodificado = decodificar_sumar_diez(paquete_sin_uno)
        elif codificacion_utilizada == "Código Gray":
            paquete_decodificado = decodificar_gray(paquete_sin_uno)
        else:
            print("Tipo de codificación desconocida. No se pudo decodificar el paquete.")
            paquete_decodificado = paquete_sin_uno

        # se agregan los paquetes decodificados al mensaje recibido
        mensaje_recibido.append(paquete_decodificado)

    print(f"Recepción y decodificación completadas. Codificación utilizada: {codificacion_utilizada}")

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
    ubicacion_json = '/Users/macbookair/Downloads/surf_report.json'  # Reemplaza 'ruta/del/archivo.json' con la ubicación real

    # fuente de información
    print("\nFuente de información")
    datos_json_original = leer_json(ubicacion_json)  # Leer el JSON
    if datos_json_original is None:
        print("Error: No se pudo cargar el archivo JSON.")
    else:
        print("Datos JSON leídos (original):", datos_json_original)

    mensaje_binario = fuenteinfo(json.dumps(datos_json_original))

    # etapa del transmisor
    print("\nTransmisor")
    # Mostrar el mensaje binario antes de la codificación
    print("Mensaje binario (antes de la codificación):", mensaje_binario)
    # Transmitir el mensaje binario con codificación Huffman y "1" al inicio de cada paquete
    mensaje_transmitido, codificacion, tipo_codificacion = transmisor_d(mensaje_binario)

    # Mostrar los paquetes transmitidos después de la codificación
    print("\nPaquetes Transmitidos (después de la codificación):", tipo_codificacion)
    print(mensaje_transmitido)
    #for paquete in mensaje_transmitido:
        #print(paquete)

    if codificacion:
        print("\nTabla de Codificación:", tipo_codificacion)
        for simbolo, codigo in codificacion.items():
            print(f"{simbolo}: {codigo}")

    # etapa del canal
    print("\nCanal")

    # se definen los canales a utilizar
    canal1 = {'nombre': "Canal 1", 'velocidad': 1000}
    canal2 = {'nombre': "Canal 2", 'velocidad': 1500}
    canal3 = {'nombre': "Canal 3", 'velocidad': 2000}
    canal4 = {'nombre': "Canal 4", 'velocidad': 1200}
    canal5 = {'nombre': "Canal 5", 'velocidad': 1300}
    canal6 = {'nombre': "Canal 6", 'velocidad': 1400}
    canal7 = {'nombre': "Canal 7", 'velocidad': 2100}
    canal8 = {'nombre': "Canal 8", 'velocidad': 1700}
    canales = [canal1, canal2, canal3, canal4, canal5, canal6, canal7, canal8]

    mensaje_recibido = canal_adaptativo(canales, mensaje_transmitido)

    # Imprimir los paquetes transmitidos
    #for paquete in mensaje_recibido:
        #print(f"Paquete transmitido: {paquete}")

    print("Mensaje recibido:", mensaje_recibido)
    len(mensaje_recibido)

    # etapa del receptor
    print("\nReceptor")
    mensaje_decodificado = receptor(mensaje_recibido, codificacion, tipo_codificacion)
    # Imprime el mensaje decodificado
    print("Mensaje decodificado:", mensaje_decodificado)
    # Convertir el mensaje decodificado en una cadena binaria completa
    mensaje_decodifica = ''.join(mensaje_decodificado)
    # Mostrar el mensaje binario recuperado
    print("Mensaje binario recibido:")
    print(mensaje_decodifica)

    # destino de la información
    print("\nDestino de la información")
    # Convertir el mensaje binario con ruido en cadena JSON
    try:
        datos_recuperados = json.loads(binario_a_cadena(mensaje_decodifica))
        print("Datos JSON recuperados:")
        destinoinfo(datos_recuperados)
    except json.JSONDecodeError:
        # Mostrar la información sin convertirla en JSON
        print("\nInformación recuperada (con ruido):")
        print(binario_a_cadena(mensaje_decodifica))
        print("El mensaje decodificado contiene un JSON inválido debido a las modificaciones.")
if __name__ == "__main__":
    main()