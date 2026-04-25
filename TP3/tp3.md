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


