# Trabajo Práctico N° 5 - Comprendiendo la arquietectura de servicios ante distintos tipos de tráfico 

## 1) Reconocimiento de arquitecturas

|  |  |  |  |
| --- | --- | --- | --- |
| ELEMENTO | ¿QUÉ PROBLEMA RESUELVE? | ¿EN QUÉ CAPA O CAPAS DEL MODELO TCP/IP PODRÍAMOS UBICAR SU FUNCIÓN PRINCIPAL? | ¿QUÉ PASARÍA SI ESE COMPONENTE FALTA EN UNA ARQUITECTURA? |
| Firewall | Analiza y filtra el tráfico de red para poder bloquear acceso no autorizados o ataques maliciosos, previniendo caídas. | Se encuentra en la **Capa de Red (Capa 3)** y de **Transporte (Capa 4)**, aunque los más avanzados actúan en la de **Aplicación (Capa 7)**. | Sin él, la infraestructura queda expuesta a intrusiones, robo de datos y caídas por saturación intencional. |
| Load Balancer | Distribuye de manera equitativa el tráfico entrante entre múltiples servidores para evitar la sobrecarga de un solo nodo. | Se ubica en la capa de **Transporte (Capa 4)** o en la de **Aplicación (Capa 7).** | No usarlo, provoca cuellos de botella, debido a que un solo servidor recibiría todas las peticiones, y agotaría sus recursos rápidamente. |
| Queue | Actúa como un búfer que añade tareas de manera asíncronas o picos de tráfico para procesarlas a un ritmo manejable. | Se ubica en la **Capa de Aplicación (Capa 7)**. | Un aumento brusco de peticiones provocaría que la memoria y CPU de los servidores se agoten, por ende, habría pérdida de datos. |
| Compute | Proporciona la capacidad de procesamiento (CPU y RAM) necesaria para ejecutar la lógica principal del sistema. | Se encuentra en la **Capa de Aplicación (Capa 7)**. | Su falta, hace que no hay aun entorno físico o virtual donde alojar y correr el código que procesa las peticiones del usuario. |
| Serverless Function | Ejecuta fragmentos de código bajo demanda en respuesta a eventos, escalando de cero a miles din gestionar servidores. | Opera en la **Capa de Aplicación (Capa 7)**. | Con su falta, se tendría que mantener obligatoriamente los servidores encendidos continuamente para tareas esporádicas, lo que aumentaría los costos operativos. |
| SQL DB | Almacena datos estructurados, con relaciones claras, asegurando integridad y transacciones (ACID). | Trabaja en la **Capa de Aplicación (Capa 7)**. | No sería posible gestionar registros críticos con consistencia y seguridad, como cuentas de usuarios o pagos. |
| NoSQL | Almacena grandes volúmenes de datos sin estructura rígida, priorizando la escalabilidad horizontal y la velocidad. | Se encuentra en la **Capa de Aplicación (Capa 7)**. | Sería ineficiente intentar guardar datos masivos y dinámicos en tabla rígidas. |
| Cache | Almacena en memoria rápidamente los resultados de consultas frecuentes para servirlos casi instantáneamente. | Su ubicación es en la **Capa de Aplicación (Capa 7)**. | Sin ello, las bases de datos recibirían consultas repetitivas, aumentando la latencia y la probabilidad de un colapso. |
| CDN | Distribuye copias de contenido estático en servidores geográficamente cercanos al usuario final para acelerar su carga. | Actúa en la **Capa de Aplicación (Capa 7)**. | Afectaría a los usuarios lejanos, que esperarían tiempos de carga muy altos y el ancho de banda del servidor principal se agotaría. |
| Storage | Provee almacenamiento de objetos a gran escala para archivos multimedia y backups y documentos pesados. | Se ubica en la **Capa de Aplicación (Capa 7)**. | Los archivos de los usuarios saturarían el almacenamiento local de los servidores de cómputo en poco tiempo. |
| Search Engine | Indexa volúmenes grandes para permitir búsquedas complejas y filtrados a muy alta velocidad. | Se ubica en la **Capa de Aplicación (Capa 7)**. | Las búsquedas dependerían de la base de datos principal, el cual es un proceso lento con un excesivo consumo de recursos. |
| Réplica | Retiene una copia sincronizada de la base de datos principal que se encarga de responder consultas de lectura. | Se sitúa en la **Capa de Aplicación (Capa 7)**. | El tráfico de lectura y escritura irían al mismo lado, lo que generaría bloqueos constantes en el procesamiento de datos. |

## 2) Tipos de tráficos

|  |  |  |  |
| --- | --- | --- | --- |
| **TIPO DE TRÁFICO** | **EJEMPLO REAL** | **COMPONENTE RECOMENDADO PARA PROCESARLO** | **RIESGO SI SE PROCESA INCORRECTAMENTE** |
| STATIC | Imágenes (png o jpg), CSS o JavaScrip de una página web. | CDN o almacenamiento estático. | Se podría desperdiciar capacidad de cómputo de los servidores de aplicación. |
| READ | Usuario consultando el feed de notician en una red social o el saldo de su cuneta. | Cache o bases de datos de Réplica. | Colapsaría la base de datos primaria por exceso de conexiones de lectura simultáneas, ralentizando el sitio. |
| WRITE | El procesamiento de un pago online, registro de una nueva cuenta o publicación de un comentario. | SQL DB, NoSQL o Queue. | Se podría dar la perdida la integridad de los datos, transacciones fallidas o la saturación de la capacidad de escritura en el disco. |
| UPLOAD | Subir una foto de perfil, un archivo adjunto pesado o un video en alta definición. | Storage. | El disco local de la instancia principal se llenaría al 100%, provocando la caída del servidor de inmediato. |
| SEARCH | Búsqueda de productos aplicando múltiples filtros dentro de un e-commerce. | Search Engine. | Se harían consultad ineficientes que paralizarían el rendimiento general de la base de datos transaccional. |
| MALICIOUS | Ataque de fuerza bruta a contraseñas o un ataque de Denegación de Servicio (DDoS). | Firewall. | Los servidores consumirían toda su CPU y ancho de banda respondiendo a bots, dejando el sistema inoperable. |

## 3) Testeando queues

Construimos la infraestructura mínima en le juego (en modo Sandbox) para testear queues:

![infraestructura-min](/TP5/img/topografia_minima_analisis_queues.png)

Vamos a jugar con el throughput (rate de tráfico) y que ocurre con la queue:

### Traffic rate por defecto

Al darle play al juego inicia con el traffic rate igual 1. Se puede observar que el funcionamiento es el siguiente: Las bolitas que se ven representan distintos tipos de tráfico:

- La bolita verde 🟢 representa tráfico del tipo STATIC
- La bolita azul 🔵 representa trafíco del tipo READ
- La bolita naranja 🟠 representa trafíco del tipo WRITE
- La bolita amarilla 🟡 representa tráfico del tipo UPLOAD
- La bolita celeste 🔷 representa tráfico del tipo SEARCH
- La bolita roja 🔴 representa un ataque 💀

Las bolitas "van saltando" por los distintos elementos de la infraestructura, los cuales son:

1. Firewall (primer elementos violeta): Es la primera línea de defensa. Bloquea tráfico malicioso.
2. Queues (segundo elemento amarillo): Es un buffer para request durante rates de tráficos pico. Previene caidas del sistema.
3. Nodo de cómputo (último cilindro naranja): Procesa los request.

![traffic-rate-por-defecto](/TP5/img/traffic_rate_default.png)

En esta primera instancia por defecto cada bolita que sale logra atrevesar todos los elementos de la infrestructura y ser procesada. La queue no se satura y se podría decir que núnca esta llena.

Vamos a incrementar el valor de traffic rate...

- Traffic Rate: 10

    ![traffic-rate-10](/TP5/img/traffic_rate_8.png)

- Traffic Rate: 20

    ![traffic-rate-20](/TP5/img/traffic_rate_20.png)

- Traffic Rate: 50 (max)

    ![traffic-rate-50](/TP5/img/traffic_rate_50max.png)


A medida que vamos aumentando el traffic rate vemos como son cada vez más los request al sistema, y como se van quedando en el buffer de la queue esperando a ser procesadas. Esto demuestra una saturación en el sistema.

Tambien vemos como las bolitas rojas que salen del origen o generador de request no pasan del firewall, demostrando como este protege de los ataques maliciosos.

Al bajar el valor de traffic rate de golpe cero ya no se generan más request pero siguen procesando los que quedaron en el buffer de la queue. Obviamente a una velocidad mucho menor en comparación que con las que se generan para valores altos de traffic rate.

## 4) Primera infraestructura mínima

Vamos a testear si la infraestrutura puede resolver valores de frecuencia más altos para todos los tipos de request. El estado inicial de la infraestructura, con el presupuesto y estado de salud de los servicios, aún sin darle play es:

![estado-inicial](/TP5/img/estado_inicial.png)

Luego de darle play, y transcurridos unos apenas 7 segundos:

![](/TP5/img/estado-post2.png)

- La reputación cayó muy rápido a 0%. 
- El estado de salud de los servicios se mantuvo intacto, pero esto quedará así debibo a que estamos en modo *snadbox*.
- El círuclo debajo del centro de cómputo se puso de color naranja, y al posicionar el mouse sobre el vemos que sale `load: 4/4`. **Indicando que se encuentra saturado**.

Hagamos algunas mejoras:
- Incluiremos un nuevo centro de cómputo, ahora tendremos dos trabajando en paralelo.
- Agregaremos una base de datos SQL.
- Y una base de datos NoSQL.
- Llevaremos el traffic rate al máximo

![](/TP5/img/estado-mejoras-2comp.png)

Con las mejora de dos cómputos esperábamos tener una mejor performance, sin embargo obtuvimos el mismo resultado e incluso un poco peor, para este caso se llegó al 0% de reputación a los 5 segundos. Nuestra suposición es que por más que haya dos centros de cómputos, no está siendo bien distruibuido el tráfico entre estos.

Apliquemos mejores técnicas...

## 5) Escalabilidad y balanceo

**Estrategia 1:** Ya vimos que agregarle un segundo centro de cómputo no mejoro el soporte del sistema. Pero podemos aplicar un **balanceador de carga**, y aprovechando que tenemos este balanceador también agregaremos más centros de cómputo.

![](/TP5/img/estrategia1.png)

El rendimiento tardó un poco más en caer, pero de igual forma se llegó a 0%. Además se puede ver como todos los centros de cómputo están saturados por el color rojo de su círculo inferior. *Al parecer más no significa mejorar... Calidad antes que cantidad?...*

**Estrategia 2:** Vamos a agregar las siguiente mejoras

- Una segunda queue
- Doble balanceador de carga
- Una memoria cache para reducir la carga de la base datos
- Un read replica. Es un respaldo para los paquetes de lectura, en caso que se caiga la base de datos original.
- Vamos a escalar los centros de cómputo verticalmente, subiendolos a tier 3.
- Y también los vamos a escalar horizontalmente, ahora tendremos 8.

Aplicamos estas mejora suponiendo un presupuesto de $2000, menor al planteado originalmente, y se pudo hacer completa la infraestruturam sobrando un poco de dinero, pero es poco de todas, no alcanzaría o no duraría mucho tiempo para mantenimiento posterior. Se debería contar con un mayor presupuesto para estas mejoras.

![](/TP5/img/estrategia2.png)

Para estas mejores se redujo el tiempo en que cae el 0%, pero de igual forma se mantiene en ese nivel, sería ideal no caer al 0%.

Probemos otro approach donde no se use tanto, sino poco de forma eficiente:

![](/TP5/img/Captura%20de%20pantalla%20de%202026-06-18%2006-44-47.png)

Con esta forma se cae al 0% de reputación. Sin embargo se puede ver que el budget suber, empezamos con 3800 y ahora tenemos $4500 aproximadamente. Y en los centros de cómputo se pueden ver de color verde, indicando que no hay saturación y estan funcionando de forma liviana. Lo ideal es buscar un equilibrio entre un escalado horizontal y vertical de los centros de cómputo, ya ambos mejoran la performance del sistema en términos de procesamiento. 
Si solo se escala horizontalmente podemos llegar a un coste de mantenimiento altísimo lo que no haría nada rentable al sistema, y si solo escalamos verticalmente concentramos demasiado los puntos de falla haciendo posible de que ante un evento inesperado se caiga el sistema.

## 6) Modo Survival

Diseñaremos una arquitectura inicial sólida y trataremos de sobrevivir lo más posible mejorando la misma en el modo "survival".

![](/TP5/img/infraestructura-final.png)

![](/TP5/img/final-score.png)

### Elección de Componentes y Tráfico Atendido

- **Firewall**: para filtrar los paquetes maliciosos e intentos de ataque.
- **Compute (centros de cómputo)**: Atiende todos los tráficos ya que pasan por el para ser procesados.
- **CDN**: para resolver los datos estáticos sin sobrecargar los sistemas propios.
- **Storage**: para ayudar al CDN con ese tipo de tráfico conectado a nuestros centros de cómputo, de manera que los estáticos necesarios se suban al storage y se mantengan ahí.
- **Queues**: para estabilizar el flujo de paquetes.
- **Load Balancer**: para distribuir equitativamente la carga sobre los centros de computos. Atiende todo tipo de paquetes.
- **Base de datos relacional**: para almacenar los datos consistentemente. Cubre las request de Read/Write/Search.
- **Cache**: para aliviar la carga de las BD permitiendo que accedan a los datos mas recientes en la cache - Cubre las request de Read/Write/Search.

### Cuello de botella - Motivo de fallo


El cuello de botella que apareció se debió al procesamiento de cómputo, para eso escalamos horizontalmente y luego verticalmente, pudiendo después seguir expandiendo. Pero de igual forma las request fueron demasiadas para soportar. Expandiendo/mejorando de otra forma se puede llegar a mejores resultados, es cuestión de seguir "jugando".
