# Trabajo Práctico N° 4 - Continuamos con infraestructura de servicios web con perspectiva de redes

## 1.a) ¿Qué es la serialización en redes de computadoras?

La **serialización**, en el contexto de redes de computadoras, es el proceso de convertir una estructura de datos en memoria (como un objeto, un diccionario, una lista, etc.) en una secuencia de bytes o de caracteres que pueda ser transmitida a través de la red y luego reconstruida en el destino. El proceso inverso se llama **deserialización**.

La serialización es necesaria porque cuando dos programas se comunican a través de una red, no pueden simplemente "pasarse" objetos de memoria como lo harían dos funciones dentro del mismo proceso. La memoria de una máquina no es accesible desde otra. Entonces, lo que hacemos es tomar esa estructura de datos, "aplanarla" en un formato lineal (una secuencia ordenada de bytes o texto), enviarla por la red dentro de la carga útil de un paquete TCP o UDP, y del otro lado el receptor toma esa secuencia y la reconstruye en una estructura de datos equivalente que pueda interpretar.

Por ejemplo: Si un cliente quiere enviarle a un servidor un mensaje que tiene un campo "grupo" y un campo "payload", no puede mandar el diccionario de Python tal cual está en memoria. En cambio, lo serializa, por ejemplo en JSON como `{"group": "grupo1", "payload": "hola mundo"}`, lo convierte en bytes (codificación UTF-8), y lo envía por el socket TCP. Del otro lado, el servidor recibe esos bytes, los decodifica a string, y parsea el JSON para reconstruir el diccionario original.
La serialización es fundamental para lograr interoperabilidad entre sistemas: el cliente podría estar escrito en Python y el servidor en Java, pero si ambos acuerdan un formato de serialización común (como JSON), pueden comunicarse sin problemas independientemente del lenguaje o la arquitectura de cada uno.

## 1.b) Diferencia entre serialización binaria y no binaria

La serialización no binaria representa los datos como texto legible por humanos. Los formatos más comunes son:

- **JSON (JavaScript Object Notation)**: Probablemente el más usado hoy en día en APIs web y servicios REST. Ejemplo:
    ```json
    {"group": "Infinity LAN - V2", "payload": "Hola mundo"}
    ```

- **XML (eXtensible Markup Language)**: Fue muy popular antes de JSON, sigue usándose en sistemas empresariales y protocolos como SOAP. Ejemplo:
    ```xml
    <message>
        <group>Infinity LAN - V2</group>
        <payload>Hola mundo</payload>
    </message>
    ```

- **YAML (YAML Ain't Markup Language)**: Muy usado en archivos de configuración (Docker Compose, Kubernetes, Ansible). Ejemplo:
    ```yaml
    group: Infinity LAN - V2
    payload: Hola mundo
    ```

**Ventajas de la serialización binaria**:
- Es legible por humanos, lo que facilita enormemente el debugging. Si se captura un paquete con Wireshark o tcpdump, se puede leer directamente qué se está enviando sin necesidad de herramientas especiales de decodificación.
- Es fácil de implementar y hay bibliotecas maduras en prácticamente todos los lenguajes.
- Favorece la interoperabilidad: cualquier lenguaje o plataforma puede parsear JSON o XML sin problemas.
- Es auto-descriptiva en muchos casos (los nombres de los campos van incluidos en el mensaje).

Desventajas de la serialización no binaria:
- Ocupa más espacio. Un número como `1000000` en JSON ocupa 7 bytes como texto, mientras que en binario (como un `uint32`) ocupa solo 4 bytes. Esto se vuelve significativo cuando se transmiten grandes volúmenes de datos.
- Es más lenta de serializar y deserializar, porque hay que parsear texto, manejar escapes, validar sintaxis, etc.
- No tiene un esquema estricto de tipos de forma nativa (en JSON un número puede ser entero o float, y eso depende del parser).

Serialización Binaria:

La serialización binaria representa los datos directamente en formato binario, es decir, como secuencias de bytes que no están pensadas para ser leídas por humanos. Los formatos más comunes son:
- **Protocol Buffers (protobuf)**: Desarrollado por Google, es muy usado en comunicaciones entre microservicios (gRPC). Requiere definir un esquema `.proto` previo.
- **MessagePack**: Es como "JSON binario". Mantiene la estructura clave-valor pero codificada en binario, resultando más compacto y rápido.
- **BSON (Binary JSON)**: Usado internamente por MongoDB. Es una representación binaria de documentos tipo JSON.
- **Apache Avro**: Muy usado en ecosistemas de Big Data (Kafka, Hadoop). Usa esquemas y es muy eficiente para serializar grandes volúmenes de datos.

**Ventajas de la serialización binaria:**
- Es mucho más compacta. Los mensajes ocupan significativamente menos bytes, lo cual reduce el ancho de banda consumido y es crítico en sistemas de alto tráfico o en conexiones limitadas (IoT, redes móviles).
- Es más rápida de serializar y deserializar, porque trabaja directamente con representaciones de bytes en lugar de parsear texto.
- Muchos formatos binarios (como protobuf) imponen un esquema estricto de tipos, lo que ayuda a detectar errores tempranamente y a mantener compatibilidad entre versiones.

**Desventajas de la serialización binaria:**
- No es legible por humanos. Si se captura un paquete con Wireshark, se verá una secuencia de bytes que no se pueden interpretar directamente sin conocer el esquema y tener las herramientas adecuadas. Esto dificulta el debugging.
- Requiere que ambos extremos (cliente y servidor) conozcan el esquema o el formato de antemano. No es auto-descriptiva (o lo es parcialmente, como en el caso de MessagePack).
- La implementación puede ser más compleja, especialmente con formatos como protobuf que requieren compilar archivos de definición de esquemas.
- Menor flexibilidad: cambiar la estructura de los datos puede requerir actualizar esquemas y regenerar código en ambos extremos.

## 2. Desplegando un servidor TCP multi-hilo

Realizamos la actividad de forma asincrónica. Lanzamos el [servidor](/TP4/scripts/server.py) y le enviamos el paquete JSON:
```json
{
    "group": "Infinity-LAN-V2", 
    "payload": "Hola desde PacketSender"
}
```

Para enviar el paquete primero utilizamos **netcat** y luego el programa **PacketSender**.

Resultados:
![registro-mensajes-al-servidor](/TP4/img/documentacion-mensajes-al-servidor.png)
