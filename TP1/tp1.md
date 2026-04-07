# Parte 1: Simulación de envío de paquetes, ARP y ruteo entre redes

## Identificación de dispositivos y armado de la topología
Inicialmente cada integrante del grupo configura su **NIC (Network Interface Card)**. 
Roles:
- Marcos: Host1
- Benjamin: Host2
- Octavio: Router por Defecto (Default Gateway)

| Device | IP Address (origin) | MAC Address (origin) | Destination MAC
|----------|-----------|----------|------------|
| Host1 (Marcos)  | 10.11.0.101  | AD:41:82   | 09:A2:31 |
| Host2 (Benjamin)| 10.11.0.102  | AA:43:15   | 09:A2:31 |
| Router por Defecto (Octavio) | 10.11.0.1 | 09:A2:31 | AA:45:92 |

El router por defecto es el encargado de comunicarse con el router central. Cada uno de los host está vinculado a este router, y a la vez el router debe contar con las direcciones internas conocidas de cada host. El router centraliza las conexiones de los host, lo que permite la comunicación interna y la salida hacía la WAN para comunicarse con otras redes.

Cuando el router recibe paquetes a enviar a los host internos de la LAN debe resolver sus direcciones físicas. Para esto se simula el envío de una APR Request por broadcast y la recepción de una ARP Reply unicast de cada host. A continuación el router genera una tabla que almacena en su memoria:

**Tabla ARP**: Tabla que el router de la LAN almacena en su memoria
| Device | IP Address| MAC Address|
|----------|-----------|----------|
| Host1 (Marcos)  | 10.11.0.101  | AD:41:82   | 
| Host2 (Benjamin)| 10.11.0.102  | AA:43:15   | 


### Conformación de paquetes
Cada integrante del grupo que representa un host tiene asignado (mediante su legajo) dos direcciones posibles de destino y un payload en hexadecimal. Se debe realizar la encapsulación siguiendo el modelo de capas, transformado los datos en un *frame ethernet* que contenía un paquete IP. Todos los frames apuntan físicamente al default gateway para iniciar el ruteo.

Host 1 (Marcos)

- MAC DESTINO: 09:A2:31
- MAC ORIGEN: AD:41:82
- IP ORIGEN: 10.11.0.101
- IP DESTINO: 10.8.0.102
- TTL: 6
- PAYLOAD: 0110 1101 1110 1000
- CRC: -

HOST 2 (Benjamin)

- MAC DESTINO: 09:A2:31
- MAC ORIGEN: AA:43:15
- IP ORIGEN: 10.11.0.102
- IP DESTINO: 10.6..0.105
- TTL: 6
- PAYLOAD: 0011 1011 0110 1101
- CRC: -

Conformados los paquetes, procedimos a la simulación del tráfico en el aula. El flujo observado fue el siguiente:
1. Cada host de nuestro grupo entrego el frame ethernet al compañero que representaba el default gateway. El frame contiene la MAC destino del default gateway y la IP destino de un host remoto.
2. El defaut gateway recibe el frame y verifica su dirección MAC.
   1. Desencapsula el frame para leer la IP de destino y obtiene el prefijo.
   2. Decrementa el TTL, pasando de 6 a 5.
   3. Consulta su tabla de ruteo y determina que paquetes deben ir al router central (también sería capaz de determinar si hay paquetes que van dentro de la misma LAN).
   4. Re-encapsulamiento: Construye un nuevo *frame ethernet* con su propia MAC de origen y la MAC del roter central como destino. Manteniendo el paquete IP original.
   Los frame ethernet ahora quedaron:

   HOST 1:
   - MAC DESTINO: AA:45:92
   - MAC ORIGEN: 09:A2:31
   - IP ORIGEN: 10.11.0.101
   - IP DESTINO: 10.8.0.102
   - TTL: 5
   - PAYLOAD: 0110 1101 1110 1000
   - CRC: -
  
    HOST 2:
     - MAC DESTINO: AA:45:92
   - MAC ORIGEN: 09:A2:31
   - IP ORIGEN: 10.11.0.101
   - IP DESTINO: 10.8.0.102
   - TTL: 5
   - PAYLOAD: 0110 1101 1110 1000
   - CRC: -
3. El paquete viaja por los routers centrales, repitiendo el proceso de TTL y posibles nuevos re-encapsulamientos.
4. Como los paquetes enviados no regresaron se estima que llegaron a su host de destino remoto. En el caso que no hubieran llegado, el router encargado de ese segmeto descartaría el paquete e informaría la imposibilidad de entrega simulando el retorno del paquete al emisor.

### Recepción de paquetes de un host externo a nuestra red
Nuestro compañero que representa al Default Gateway recibió un frame desde el router central. 

**Paquete recibido**:
![paquete-recibido](/TP1/img/WhatsApp%20Image%202026-03-22%20at%2012.49.07.jpeg)

Verificó en su tabla ARP y encontró que la IP 10.11.0.102 pertenece a nuestra LAN, en específico al Host2 (Benjamin). Re-encapsuló el paquete en un frame final con la MAC de destino del Host2. 

### Reflexiones y documentación

a. Durante el laboratorio, la dirección IP destino del paquete se mantuvo constante mientras que la
dirección MAC destino cambió en cada salto. ¿Por qué ocurre esto y qué nos dice sobre la diferencia entre direccionamiento lógico (IP) y direccionamiento físico (MAC)?
---
Esto pasa porque la dirección IP se usa para identificar al destino final del paquete, o sea, a qué equipo o red tiene que llegar, y por eso no cambia durante el recorrido.
En cambio, la dirección MAC se usa solo para la comunicación dentro de cada enlace local. Entonces, cada vez que el paquete pasa por un router, ese router le saca la trama anterior y lo vuelve a encapsular en otra nueva con una MAC de destino distinta, que corresponde al siguiente salto.

En otras palabras, la IP sirve para el envío de extremo a extremo entre redes, mientras que la MAC sirve solo para mover el paquete de un dispositivo a otro dentro de la red local de ese momento.
Esto muestra que el direccionamiento lógico (IP) es global y se mantiene, mientras que el direccionamiento físico (MAC) es local y va cambiando en cada salto.


  
b) Cuando un host quiere enviar un paquete a un dispositivo en otra red, no intenta descubrir directamente la MAC del host destino, sino la del default gateway. ¿Por qué se utiliza este mecanismo y qué problema resolvería el gateway que el host no puede resolver por sí solo? 
---
Se usa ese mecanismo porque el host solo puede conocer las MAC que están dentro de su misma red local. Si el paquete va hacia otra red, el equipo se da cuenta por la máscara de subred de que ese destino no está en su LAN, entonces en vez de buscar la MAC del destino final, busca la MAC del gateway para mandárselo a él.

El default gateway resuelve un problema que el host por sí solo no puede: saber por dónde seguir el camino hacia otras redes. El host no tiene información completa de rutas ni sabe cómo llegar a redes lejanas, mientras que el router sí tiene esa lógica y puede reenviar el paquete al siguiente salto hasta que llegue al destino.

En resumen, el host solo sabe moverse bien dentro de su red local; para salir de ella necesita entregarle el paquete al gateway, que es el encargado de conectarlo con redes externas.

c) Cada router toma decisiones basándose únicamente en su tabla de ruteo local y no en el camino completo hacia el destino. ¿Qué ventajas tiene este modelo de ruteo hop-by-hop para redes grandes como Internet?
---
La ventaja de este modelo es que hace posible que redes enormes como Internet funcionen sin que cada router tenga que conocer todo el recorrido completo. Cada router solo necesita saber cuál es el próximo salto más conveniente según su tabla de ruteo.

Esto hace que la red sea más escalable, porque no obliga a guardar toda la topología de Internet en cada equipo. Además, le da más flexibilidad y tolerancia a fallos, ya que si una ruta se cae o cambia, los routers pueden actualizar sus tablas y seguir enviando los paquetes por otro camino sin que el host de origen tenga que hacer nada.

En resumen, el ruteo hop-by-hop simplifica el funcionamiento de la red y permite que Internet siga operando aunque haya cambios o fallas en distintas partes.

d) En el laboratorio observamos que los routers desencapsulan y vuelven a encapsular el paquete en cada
enlace. ¿Por qué es necesario reconstruir el frame Ethernet en cada salto y qué ocurriría si los routers intentaran reenviar exactamente el mismo frame?
---
Es necesario reconstruir el frame Ethernet en cada salto porque ese frame solo sirve para el enlace local actual. Las direcciones MAC que lleva adentro representan únicamente al emisor y al receptor de ese tramo de red, no al destino final de todo el recorrido.

Por eso, cuando el paquete llega a un router, este quita el frame anterior, revisa la dirección IP para decidir a dónde mandarlo, y después lo vuelve a encapsular en un frame nuevo con la MAC del siguiente salto.

Si el router intentara reenviar exactamente el mismo frame, no funcionaría, porque las MAC seguirían siendo las del enlace anterior. Entonces el siguiente dispositivo no lo reconocería como dirigido a él y lo descartaría.

e) El campo TTL se decrementa en cada router. ¿Qué problema de la red previene este mecanismo y qué
podría suceder si el TTL no existiera?
---
El TTL sirve para evitar que un paquete quede dando vueltas de forma infinita en la red. Esto puede pasar, por ejemplo, si hay un bucle de ruteo o una mala configuración entre routers.

Cada vez que el paquete pasa por un router, el TTL se reduce en 1. Cuando llega a 0, el paquete se descarta. De esa forma se evita que siga ocupando ancho de banda y procesamiento innecesariamente.

Si el TTL no existiera, un paquete podría circular sin fin por la red, generando tráfico inútil y hasta saturando enlaces y routers.

# Parte 2: Inyección y detección de errores

Esta segunda parte consistió en aprender en la forma en la que se detectan errores en la transmición de datos.

Uno de nosotros recibió el payload C388, y debía enviarlo al IP de destino 192.168.1.200, que corresponde al compañero con el que estamos realizando esta actividad. 
La técnica de detección de errores que vamos a utilizar el XOR, por lo tanto nos queda lo siguiente:

C388h -> 1100001100010001b

Y tenemos que hacer el XOR entre los nibbles:

1100 `XOR` 0011 = 1111

1111 `XOR` 1000 = 0111

0111 `XOR` 1000 = 1111

Entonces el CRC es 1111

![frame-ethernet](/TP1/img/Captura%20desde%202026-04-06%2019-12-35.png)

Luego este payload se vio afectado al modificar uno o algunos bits por el profesor. En específico se vio modificado el primer y tercer nibble, siendo el payload ahorta C781. Pero este error lo deberá identificar nuestro compañero que recibió nuestro mensaje.

A nosotros nos llegó un mensaje de el, con un payload y un CRC. Debemos verificar que sea correcto:

![payload-recibido](/TP1/img/Captura%20desde%202026-04-06%2019-17-48.png)

Ya se puede ver en el desarrollo que hicimos en clase pero:

- Payload recibido: F2A0h -> 1111001010100000b
- CRC: 0000

Lo que tiene en particular es que nuestro compañero utilió bit de paridad para la detección de errores, por lo tanto tenemos que verificar utilizando esta técnica.

La técnica de bit de paridad consiste en asignar un bit en cada nibble según la cantidad par o impar de "1" que tenga. Si tiene una cantidad de "1" par entonces se asigna el bit 0, y si la cantidad es impar se asigna el bit 1.
Para el payload recibido:

- 1111 -> Cuatro "1", cantidad par -> Bit de paridad 0
- 0010 -> Un "1", cantidad impar -> Bit de paridad 1
- 1010 -> Dos "1", cantidad par -> Bit de paridad 0
- 0000 -> No hay "1", se considera par -> Bit de paridad 0

Entonces nos queda 0100. Pero el CRC dice que es 0000, por lo tanto podemos detectar un error, y podemos ver que es en el tercer nibble (de der. a izq.).

La ventaja del bit de paridad con respecto a XOR es que podemos identificar en que nibble ocurre el error. Pero tiene desventajas considerables:

El payload se modificó pasando el tercer nibble de 0011 (3) a 0010 (2), se modificó solo un bit. Pero si se hubiesen modificado dos bits, por ejemplo pasando de 0011 (3) a 1010 (10) los bits de paridad hubiesen resultado 0000, y uno tendería a pensar que se recibió el dato correcto, pero no va a ser el caso. Esta es una muy fuerte debilidad de el bit de paridad.

