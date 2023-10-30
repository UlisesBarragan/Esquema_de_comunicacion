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

# Función para dividir un mensaje binario en paquetes de 8 bits
def dividir_en_paquetes(binario, longitud_paquete=8):
    paquetes = [binario[i:i+longitud_paquete] for i in range(0, len(binario), longitud_paquete)]
    return paquetes

# Función para agregar un 1 al inicio del mensaje binario
def transmisor(binario):
    paquetes = dividir_en_paquetes(binario)  # Dividir el mensaje binario en paquetes de 8 bits
    mensaje_codificado = []
    for paquete in paquetes:
        mensaje_codificado.append('1' + paquete)  # Agregar "1" al inicio de cada paquete
    return mensaje_codificado

# Función que simula un canal con ruido de modificación y calcula la entropia 
def canal(mensaje_codificado, probabilidad_error):
    print("Iniciando transmisión a través del canal de cable coaxial....")

    mensaje_recibido = []
    paquetes_con_ruido = 0  # Inicializar el contador de paquetes con ruido

    for paquete_codificado in mensaje_codificado:
        paquete_recibido = "1"  
        paquete_tiene_ruido = False  # Inicializar como False para el paquete actual

        for bit in paquete_codificado[1:]: 
            # Se genera un numero aleatorio para decidir si se introduce ruido
            numero_aleatorio = random.random()

            # Introducir errores aleatorios en el bit
            if numero_aleatorio < probabilidad_error:
                bit_recibido = '0' if bit == '1' else '1'
                paquete_tiene_ruido = True  # Establecer en True si hay ruido en el paquete
            else:
                bit_recibido = bit

            paquete_recibido += bit_recibido  # Agregar el bit al paquete recibido

        mensaje_recibido.append(paquete_recibido)  # Agregar el paquete recibido

        # Verificar si el paquete actual tiene ruido y contarlos
        if paquete_tiene_ruido:
            paquetes_con_ruido += 1

    # Calcular la probabilidad de que un paquete tenga ruido
    probabilidad_paquete_con_ruido = paquetes_con_ruido / len(mensaje_codificado)

    # Calcular la entropía H(x) = -sum(p(k).log2(p(k)))
    entropia = -probabilidad_paquete_con_ruido * math.log2(probabilidad_paquete_con_ruido) if probabilidad_paquete_con_ruido > 0 else 0

    return mensaje_recibido, entropia

# Función para decodificar el mensaje y eliminar el primer 1
def receptor(mensaje_codificado):
    print("Iniciando recepción y decodificación del mensaje...")
    mensaje_recibido = []
    
    for paquete_codificado in mensaje_codificado:
        print(f"Paquete codificado recibido: {paquete_codificado}")
        
        paquete_decodificado = paquete_codificado[1:]  # Eliminar el "1" del inicio
        mensaje_recibido.append(paquete_decodificado)
    
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
    datos_json_original = leer_json(ubicacion_json)  # Leer el JSON
    if datos_json_original is None:
        return

    print("Datos JSON leídos (original):", datos_json_original)

    # transmisor
    mensaje_binario = fuenteinfo(json.dumps(datos_json_original))
    mensaje_codificado = transmisor(mensaje_binario)
    # canal
    mensaje_recibido, entropia = canal(mensaje_codificado, probabilidad_error=0.1) 
    # receptor
    mensaje_decodificado = receptor(mensaje_recibido)
    # Convertir el mensaje decodificado en una cadena binaria completa
    mensaje_decodificado = ''.join(mensaje_decodificado)
    # Mostrar el mensaje binario con ruido
    print("Mensaje binario con ruido:")
    print(mensaje_decodificado)
    
    # destino de la información
    # Convertir el mensaje binario con ruido en cadena JSON
    try:
        datos_recuperados = json.loads(binario_a_cadena(mensaje_decodificado))
        print("Datos JSON recuperados:")
        destinoinfo(datos_recuperados)
    except json.JSONDecodeError:
        # Mostrar la información sin convertirla en JSON
        print("\nInformación recuperada (con ruido):")
        print(binario_a_cadena(mensaje_decodificado))
        print("El mensaje decodificado contiene un JSON inválido debido a las modificaciones.")
    
    print(f"Entropía debida a ruido en el canal: {entropia:.2f}")

if __name__ == "__main__":
    main()