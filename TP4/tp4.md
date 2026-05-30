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

## 3. Programando una aplicación de cliente que permite el envio de mensajes a través de una consola

Viendo el [client.py](https://drive.google.com/file/d/10USHnqU7sAeFWQ4Y4Ma8kzydM6YnDhoe/view?usp=drive_link) que se nos dió en el Drive de la materia se nota que está incompleto: envía un solo mensaje hardcodeado con campos que no coinciden con el formato que espera el servidor (`"nombre"` y `"que_digo"` en lugar de `"group"` y `"payload"`), y se cierra inmediatamente.

Vamos a convertirlo en un cliente iteractivo:

1. El ejemplo tiene `HOST` y `PORT` hardcodeados. Necesitamos que el usuario los pueda ingresar, ya sea como argumentos de línea de comandos o preguntando al inicio. Vamos a utilizar `argparse` que es la forma estandar de Python para manejar argumentos de línea de comandos, nos permite hacer cosas como `python3 client.py --host 192.168.0.10 --port 5000` y si no pasamos nada usa valores por defecto.

2. El servidor valida que el mensaje sea un diccionario JSON con las claves `"group"` (string) y `"payload"` (string). Si el formato no coincide, el servidor imprime `"ill formatted message"`. Entonces nuestro cliente tiene que armar el JSON con esa estructura exacta antes de enviarlo.

3. En vez de mandar un solo mensaje y cerrar, necesitamos un loop que lea mensajes del usuario por consola y los envíe al servidor uno por uno, hasta que el usuario decida salir.

Se puede ver como quedo el script en [client.py](/TP4/scripts/client.py).

Para ejecutarlos primero hay que tener el servidor corriendo en otra terminal. Y despues en otra terminal ejecutamos el cliente:

![](/TP4/img/servidor-cliente-defecto.png)

## 4. Cifrando el payload

Para hacer el cifrado del payload vamos a usar **AES (Advanced Encryption Standard)** que es el estándar de cifrado simétrico más usado en el mundo real (WiFi WPA2, HTTPS, VPNs, WhatsApp, etc.). Específicamente vamos a usar la implementación **Fernet** de la biblioteca `cryptography` de Python, que internamente usa **AES-128** en modo **CBC** con **HMAC-SHA256** para autenticación.

Sus características principales son:

- Cifrado simétrico: usa la misma clave para cifrar y descifrar. Ambas partes (cliente y servidor) deben compartir la clave de antemano.
- **AES-128-CBC**: AES (Advanced Encryption Standard) es el algoritmo de cifrado por bloques más utilizado mundialmente. Opera con bloques de 128 bits. El modo **CBC** (**Cipher Block Chaining**) encadena cada bloque con el anterior, de modo que bloques idénticos de texto plano producen bloques cifrados distintos.
- **IV** (**Vector de Inicialización**): Fernet genera un IV aleatorio de 128 bits para cada operación de cifrado. Esto garantiza que cifrar el mismo texto plano dos veces con la misma clave produce resultados diferentes, evitando ataques de análisis de patrones.
- **HMAC-SHA256**: además de cifrar, Fernet calcula un código de autenticación (HMAC) sobre el texto cifrado. Esto permite al receptor verificar que el mensaje no fue alterado en tránsito (integridad) y que fue producido por alguien que conoce la clave (autenticación).
- **Timestamp**: el token Fernet incluye una marca de tiempo, lo que permite implementar expiración de tokens si se desea.
- **Salida en Base64**: el token cifrado se codifica en Base64, lo que lo hace seguro para incluir en formatos de texto como JSON, XML, o URLs.

La estructura del token Fernet es: `Version || Timestamp || IV || Ciphertext || HMAC`.

El flujo es así:

1. Se genera una clave simétrica (una secuencia de bytes aleatoria). Esta clave la tienen que conocer tanto el cliente como el servidor.
2. Para cifrar, se toma el texto plano, se lo pasa por Fernet con la clave, y devuelve un token cifrado en Base64.
3. Para descifrar, se toma el token cifrado y la misma clave, y se recupera el texto original.

Es cifrado simétrico: la misma clave sirve para cifrar y descifrar. Esto es distinto del cifrado asimétrico (como RSA) donde tenés un par de claves pública/privada.

Primero generearemos la clave que vamos a usar:

![](/TP4/img/clave-fernet.png)

Hay que modificar [client.py](/TP4/scripts/client.py) para agregar la parte de cifrado.

![comunicacion-encriptado](/TP4/img/comunicacion-encriptada.png)

## 5. Haciendo el servido capaz de decifrar el mensaje

Al [server.py](/TP4/scripts/server.py) del Drive lo modificamos agregandole le capacidad de decifrar el payload. Para esto, la clave tiene que ser la misma que usa el cliente.

Podemos ver como funciona:

![descifrando-mensajes](/TP4/img/descifrado-de-paquetes.png)

Y capturamos estos paquetes con Wireshark para ver que en efecto el payload esta siendo encriptado y el servidor es capaz de descrifrar el payload:

![captura-paquetes-encriptados](/TP4/img/captura-paquete-encriptado.png)

