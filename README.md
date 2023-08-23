# Esquema_de_comunicacion
Ulises Barragan de la Cruz (200300681)
programa que simule los 5 componente del esquema de comunicación planteado por Shannon:  
Fuente de información, Transmisor, Canal, Receptor, Destino de información. 

Esquema de comunicación 

1. Fuente de información:
   
   La api de surfline (https://www.surfline.com/) es un sitio web que proporciona información y pronósticos sobre el estado de 
   las olas para los surfistas.
   Crearia un dataframe que contenga información sobre determinada playa en una fecha en especifico, por ejemplo el pronostico  
   del clima, tamaño de las olas, dirección de las olas, etc. Después crear un json con el dataframe y ese json pasarlo a binario.

3. Transmisor:
   
   Los datos binarios se codificaran agregando un 1 al inicio del mensaje para el envio. No se uso el empaquetamiento.

4. Canal:
   
   Los datos codificados seran enviados por el canal que simulara un cable coaxial y el Ruido sera de velocidad retrasando el 
   envio de los datos 3s.

5. Receptor:

   Decodifica los datos binarios eliminando el 1 al inicio del mensaje y pasa esos datos binarios de un json.

6. Destino de información:
   
   Visualiza el dataframe con los datos obtenidos de la api de surfline.

