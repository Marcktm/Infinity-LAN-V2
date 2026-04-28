# Trabajo Práctico N° 3: "Introducción a infraestructura de servicios web con perspectiva en redes"

## Investigación conceptual: SSH

### ¿Qué es SSH?

`SSH` o **Secure Shell**, es un protocolo de administración remota que le permite a los usuarios controlar y modificar sus servidores remotos a través de internet con un mecanismo de autenticación.

Proporciona un mecanismo para autenticar un usuario remoto, transferir entradas desde el cliente al host y retransmitir la salida de vuelta al cliente. El servicio se creo como un reemplazo seguro para el Telnet sin cifrar, y utiliza técnicas criptográficas para garantizar que todas las comunicaciones hacia y desde el servidor remoto sucedan de manera encriptada.

### Diferencia entre autenticación y cifrado
- Cifrado: La privacidad.
    El cifrado se encarga de la confidencialidad. Consisten en tomar datos legibles y transformarlos en un código incomprensible usando un algoritmo matemático y una clave.

- Autenticación: La identidad.
    Es el mecanismo mediante el cual se demuestra que eres quien dices ser, y que tienes permiso para acceder al sistema.

**Primero se cifra, es decir se establece el canal seguro, y luego se autentica, es decir se identifica el usuario a través de ese canal seguro.**

### ¿Qué es una clave pública y una privada?
Antes de usar `SSH` los usuarios deben generar un par de claves criptográficas, una pública y una privada. La clave pública se comparte con el servidor, mientras que la clave privada se guarda en forma segura en el equipo del usuario.

### ¿Por qué la clave privada no debe compartirse?
Primero debemos entender el uso de las claves:

1. La clave pública se envia al cliente, mientras que la clave privada se guarda de forma segura en el servidor.
2. Luego el cliente cifra una clave de sesión aleatoria utilizando la clave pública del servidor y la envía de regreso al servidor.
3. **El servidor descifra la clave de sesión utilizando su clave privada** y envía un acuse de recibo al cliente.

**Lo que bloquea la clave pública, solo la clave cifrada lo puede desbloquear.** Es imposible (con la tecnología actual) adivinar la clave privada a partir de la clave pública.
Por esta razón la clave privada no debe compartirse a un tercero.

### ¿Qué ventajas tienen las claves SSH frente a contraseñas?
Aunque las contraseñas han sido el estándar durante décadas, en el mundo de los servidores y la infraestructura, las claves SSH las superan en dos frentes principales: **seguridad extrema** y **comodidad**.

Algunas ventajas:

1. Inmunidad a los ataques de "fuerza bruta": Un ataque de fuerza bruta ocurre cuando un programa automatizado intenta miles de contraseñas por segundo.
2. Inmunidad al phising:
    - Alguien puede crear una pantalla falsa de inicio de sesión para ingresar la contraseña.
    - La ventaja con SSH es que la clave privada núnca sale de la computadora. El servidor y la máquina se comunican matemáticamente en segundo plano.
3. Automatización. `SSH` permite la autenticación passwordless. Los scripts, las herramientas de despliegue y los programas pueden conectarse entre servidores de forma segura y automática sin intervención humana.

## Poniendo en práctica el protocolo SSH

Reservamos un par de máquinas virtuales para realizar esta actividad. Como prueba de la conexión exitosa a las computadoras mediante SSH, creamos una carpeta con el nombre de nuestro grupo en las dos VMs que tenemos acceso (PC3 y PC4):

### Conexión PC3
![conexion-SSH-PC3](/TP3/img/conexió-exito-pc3.jpeg)

### Conexión PC4
![conexion-SSH-PC4](/TP3/img/conexion-exito-PC4.png)

## Usando Wireshark para capturar tráfico SSH

SSH corre por defecto en el **puerto 22**, usando TCP. Wireshark tiene un lenguaje de filtros útiles, de los cuales para SSH podemos utilizar:
```
tcp.port == 22
```
Este muestra todo el tráfico TCP que pase por el puerto 22, tanto origen como destino.

### Tráfico capturado al conectarnos a la VM-PC3
![trafico-conexcion-pc3](/TP3/img/wireshark-paquete-octa.jpeg)

### Tráfico capturado al conectarnos a la VM-PC4
![trafico-conexcion-pc4](/TP3/img/captura-ssh-wireshark.png)

### Analizando la captura SSH

Antes de que SSH haga absolutamente nada, TCP tiene que establecer la conexión. Son los primeros tres paquetes:
```
1564  192.168.0.225 → 34.130.32.165   TCP   [SYN]
1571  34.130.32.165 → 192.168.0.225   TCP   [SYN, ACK]
1572  192.168.0.225 → 34.130.32.165   TCP   [ACK]
```
- `SYN`: La PC local le dice a la VM "*quiero conectarme*"
- `SYN-ACK`: La VM responde "*OK, acepto la conexión*"
- `ACK`: La PC local confirma "*recibido*"

Se puede observar que la PC local usó el puerto **45426** (elegido al azar) y la VM está escuchando el **puerto 22** (SSH). Esto se puede ver en la columna info: `45426 -> 22`.

**Negociación de algoritmos, Key Exchange (paquetes 1580 al 1589)**

```
1580  Client: Key Exchange Init
1581  Server: Key Exchange Init
1585  Client: Elliptic Curve Diffie-Hellman Key Exchange Init
1587  Server: Elliptic Curve Diffie-Hellman Key Exchange Reply, New Keys, Encrypted packet
1589  Client: New Keys
```

**Key Exchange Init (ambos lados)**: Cada lado envía una lista de algoritmos que soporta, en orden de preferencia: algoritmos de cifrado, de MAC (integridad), de compresión, y el método de intercambio de claves.

**Diffie-Hellman sobre Curva Elíptica (ECDH)**: Es el mecanismo matemático por el cual ambos lados acuerdan una clave secreta compartida sin nunca transmitirla por la red. Cada lado genera un número aleatorio, hace operaciones con él, se intercambian los resultados, y de esos resultados ambos pueden calcular la misma clave secreta — pero nadie que esté mirando el tráfico puede calcularla. Esto resuelve el problema fundamental de "cómo nos ponemos de acuerdo en una clave si alguien está escuchando".

**New Keys**: Es el aviso de que a partir de este paquete, todo va cifrado. Es el punto de quiebre.

Luego podemos observar que todo está cifrado
```
1597  Client: Encrypted packet (len=52)
1600  Server: Encrypted packet (len=52)
1601  Client: Encrypted packet (len=52)
```

Wiresharl solo puede decirnos el tamaño del paquete, nada del contenido.

Analizando un paquete con `Encrypted packet`
![analisis-de-paquete](/TP3/img/analisis-paquete.png)

El flag PSH (Push) significa que hay datos reales adentro, no es un ACK vacio. Son 36 bytes de payload, pero completamente cifrados

Si podemos ver metadatos:
- Quién habla: 192.168.0.225 → 4.206.219.90 — la PC local hacia la VM
- Puerto destino: 22 — confirma que es SSH
- TTL: 64 — origen Linux
- Seq: 31443, Ack: 85889 — números de secuencia TCP, dicen cuántos bytes se intercambiaron hasta este punto
- Window: 85 → escalado por 1024 = 87040 bytes de ventana disponible

**¿Es posible descifrar el contenido?**

En condiciones normales, no. Y esto está en el hex dump de abajo. 
SSH usa cifrado simétrico (típicamente AES-256 o ChaCha20) con una clave que se negoció durante el Diffie-Hellman que vimos antes. Sin esa clave de sesión, no hay forma computacionalmente viable de romperlo.

## Despliegue de servidores con netcat

Primero verificamos tener netcat tanto en la PC local como en la VM
![servidorTCP-VM](/TP3/img/servidorTCP-enVM.png)

**Levantando el servidor TCP en la VM, conexión desde la PC local y envio de mensajes**
![conexion-tcp-vm-pclocal](/TP3/img/envio_mensajes_tcp.png)

**¿Se puede descruifrar el contenido?**

Si. Netcat no cifra nada, es texto plano purdo. En Wireshark se van a ver los paquetes con protocolo TCP y si hacemos click en uno que tenga datos, en el panel hexadecimal se verá el texto directamente:

![descrifrado-netcat](/TP3/img/descifrado-contenido-tcp.png)

### UDP

Diferencia entre UDP y TCP: UDP no tiene handshake. No hay SYN, SYN-ACK, ACK, simplemente se mandan diagramas. No hay garantía que lleguen, no hay orden, no hay conexión establecida. Por esto en Wireshark se van a ver directamente los datos.

![comuniucacion-udp](/TP3/img/comunicacion-udp.png)

Y en Wireshark vemos
![wireshark-udp](/TP3/img/wireshark-udp.png)

### Dos VMs chateando entre sí

Vamos a conectarnos a las dos VMs (en terminales distintas) y establecer conexión con netcat entre ellas.

![chat-entre-VMs](/TP3/img/chat-entre-VMs.png)

### Desplegando un servidor HTTP de forma remota

Conectadonos a una de las VMs asignadas, vamos a generar un `index.html` dentro de la carpeta que generamos con el nombre de nuestro grupo.

En la PC3:

![index-enVM](/TP3/img/index_html_en_VM.png)

Desplegamos el servidor en el puerto `5500` con el comando
```bash
python3 -m http.server 5500
```

![server-desplegaod-puerto-5500](/TP3/img/server-desplegado.png)


## Man In the Middle y Principio de Confidencialidad en las Redes de Computdoras

Se vió el video de [Veritasum en YouTube](https://www.youtube.com/watch?v=PPJ6NJkmDAo). Este video aborda el problema que llama el hombre del medio, que toma vulnerabilidades en la comunicación NF entre un iphone y una terminal de pago.

### Relación con TP 1:
En el TP1, se aprendió que la información se pasaba (“viaja”) en paquetes, que es el encapsulamiento, con un contenido que se llama payload.  En el video quien hackeaba hacia lo mismo como lo que se aplico en la parte 2 de este TP, ya que se interceptaba el paquete y se cambiaban bits específicos de la payload para engañar al sistema, es decir, que en el video se cambiaria bits para engañar al iPhones y poder hacer que hiciera el cobro.


### Relación con TP 2:
En este TP, se trato la parte física, donde se usaron cables, conectores y como estos hacen viajar la información. En el video, la información que se interceptaba se hacia con proximidad física, mediante NFC, que es básicamente mediante un campo electromagnético, entonces el atacante debía interceptar por ese medio, entonces el atacante usa un aparto llamado Proxmark, que ayuda a crear un puente inalámbrico entre el teléfono y el que quiere manipular, como construir un puente entre la comunicación entre los dos dispositivos que intercambian información (ya mencionados), para actuar desde ese puente.

### Relación con TP3:
Este TP, se observó que si se usa un protocolo HTTP, cualquiera puede leer la información e intervenir, pero si se usa SSH, la información va cifrada y sería imposible leer.  Lo mismo pasa en el caso del video, porque la información porque Visa envía parte de la información sin cifrar para poder ser compatible con todo el mundo. Y se aprendió las claves publica y privadas, que en el video se explica que si Visa optara siempre por una firma digital, el lector se daría cuenta de que el mensaje fue alterado y rechazaría el pago que es lo que hace Mastercad para evitar este robo.

### ¿Qué cosas deberíamos tener en cuenta dado el principio de confidencialidad en las redes de computadoras y los resultados obtenidos en este laboratorio?

La confidencialidad y la integridad de la información, deben ser mutuas, ya que si la información viaja siendo fácil de leer como se capturo en el TP3 con el protocolo HTTP, siendo que cualquier persona en el medio puede interceptarla y manipular los bits del paquete tal como se hizo en el TP1. El video muestra que aunque se confíe en la seguridad de nuestro celular, como de que está bloqueado, porque si el protocolo no usa herramientas como las firmas digitales para validar que el mensaje no fue alterado, un atacante puede engañar al sistema cambiando bits para autorizar un pago fraudulento.
