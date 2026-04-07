# Parte 1: Armado y verificación de cables Cat5/Cat5e bajo estándar T568A/B

La actividad consitió en armar y crimpar un cable ethernet bajo la norma T568A/B derecho no cruzado.

El proceso consistió en "pelar" el cable y descubrir los cables de colores que tiene en el interior. Con estos "cables de colores" seguimos la norma para el armado. Pasamos a separar lo cables e intentar que ingresen al cabezal de ethernet sin que se desordenen... Consideramos esta como la parte más dificil 😅...

**Resultados**:

![cable-hecho](/TP2/img/WhatsApp%20Image%202026-03-31%20at%2014.23.55.jpeg)
![tester-cable](/TP2/img/WhatsApp%20Image%202026-03-31%20at%2014.23.59.jpeg)

Pudimos corroborar con el tester para cables ethernet que hicimos bien el procedimiento.

# Parte 2: Equipamiento físico, verificación y utilización de red y análisis de tráfico.

## Características principales del Cisco Catalyst 2950

**Tipo de switch**:
- Switch gestionable (managed) de capa 2
- Configuración fija (no modular)
- Orientado a redes pequeñas y medianas (edge de la red)

**Puertos y conectividad**:
- 12, 24 o 48 puertos Fast Ethernet (10/100 Mbps)
- Algunos modelos incluyen uplinks:
    - Gigabit fibra (1000BASE-SX)
    - Gigabit cobre (10/100/1000BASE-T)

**Rendimiento**:
- Switching fabric hasta 13.6 Gbps
- Forwarding a wire-speed (sin pérdida de paquetes)
- Hasta ~10 Mpps dependiendo del modelo

**Seguridad**:
Incluye varias capas de seguridad
- Port Security (por MAC)
- 802.1X (autenticación por puerto)
- SSHv2 (administración segura)
- Soporte para RADIUS / TACACS+
- VLANs privadas (aislamiento de puertos)

**QoS (Calidad de Servicio)**:
- Priorización por 802.1p (CoS)
- 4 colas por puerto
- Algoritmos:
    - Strict Priority
    - Weighted Round Robin (WRR)

**VLANs y switching avanzado**:
- Soporte IEEE 802.1Q (VLAN tagging)
- VTP (VLAN Trunking Protocol)
- STP, RSTP, PVST+ (evitar loops)
- EtherChannel (agregación de enlaces)

**Manejo de tráfico multicast**:
- IGMP Snooping v3
- Optimiza tráfico multicast

**Administración**:
- CLI (Cisco IOS)
- Web (Cisco Device Manager)
- SNMP
- Software: Cisco Network Assistant

**Alta disponibilidad**:
- Spanning Tree + mejoras (UplinkFast, BackboneFast)
- Redundancia de enlaces
- Soporte de fuente redundante (RPS)

**Características físicas**:
- Formato rack 1U
- Consumo bajo (~30–45W)
- Fuente interna + opción redundante


## Configuración del switch y conexión entre computadores

Para este punto, uno de los grupos se encargó de configurar el switch al conectar su PC al puerto de consola, utilizando el software PUTTY.

Luego accedieron a las opciones de administración del switch para modificar las claves de acceso:

> La siguiente demostración fue realizada por otro grupo, sin embargo estuvimos presentes para presenciar como fue el procedimiento

```
ip subnet-zero
!
!
spanning-tree mode pvst
no spanning-tree optimize bpdu transmission
spanning-tree extend system-id
!
!
!
!
interface FastEthernet0/1
!
interface FastEthernet0/2
!
interface FastEthernet0/3
!
interface FastEthernet0/4
!
interface FastEthernet0/5
!
interface FastEthernet0/6
!
interface FastEthernet0/7
 switchport access vlan 2
 switchport mode access
 spanning-tree portfast
!
interface FastEthernet0/8
 switchport access vlan 2
 switchport mode access
 spanning-tree portfast
!
interface FastEthernet0/9
!
interface FastEthernet0/10
 switchport access vlan 2
 switchport mode access
!
interface FastEthernet0/11
 switchport access vlan 2
 switchport mode access
!
interface FastEthernet0/12
 switchport mode trunk
!
interface FastEthernet0/13
!
interface FastEthernet0/14
!
interface FastEthernet0/15
 switchport access vlan 2
 switchport mode access
!
interface FastEthernet0/16
!
interface FastEthernet0/17
!
interface FastEthernet0/18
 switchport access vlan 2
 switchport mode access
!
interface FastEthernet0/19
!
interface FastEthernet0/20
!
interface FastEthernet0/21
!
interface FastEthernet0/22
!
interface FastEthernet0/23
!
interface FastEthernet0/24
!
interface Vlan1
 ip address 192.168.1.2 255.255.255.0
 no ip route-cache
 shutdown
!
interface Vlan2
 ip address 192.168.2.10 255.255.255.0
 no ip route-cache
!
ip default-gateway 192.168.1.1
ip http server
!
line con 0
line vty 0 4
 login
line vty 5 15
 login
!
!
!
monitor session 1 source interface Fa0/7 , Fa0/10
monitor session 1 destination interface Fa0/11
monitor session 2 destination interface Fa0/8
end


```

Con la configuración global `ip subnet-zero` permite usar subredes con todos ceros.
Luego configura las interfaces. Se configuran puertos en VLAN2, en específico:

- Fa0/7, Fa0/8 → con PortFast
- Fa0/10, Fa0/11
- Fa0/15
- Fa0/18

Luego podemos ver:
```
interface Vlan2
 ip address 192.168.2.10 255.255.255.0
```

- Tenmos la IP de gestión del switch
- Se encuentra en la VLAN donde están los hosts

Luego se configura el gateway por defecto: `ip default-gateway 192.168.1.1`

Por nuestra parte lo que hicimos fue conectarnos a un puerto de consola del switch para testear la conectividad. Para hacerlo utilizamos los cables que hicimos en la parte 1.

Una vez la computadora conectada al switch utilizamos el comando `ip a`:

![comando-ip-a](/TP2/img/WhatsApp%20Image%202026-03-31%20at%2014.55.26.jpeg)

Y con esto creamos un perfil IPv4 para ponernos en la misma red que el switch y de esa forma nos podamos comunicar.


![](/TP2/img/WhatsApp%20Image%202026-03-31%20at%2014.53.52.jpeg)
Otra grupos hicieron lo mismo y gracias a esto podemos comunicarnos entre nosotros.

Nosotros tenemos la dirección IP `192.168.2.12`, mientras que otro grupo que tambien se conectó al switch tiene la dirección `192.168.2.11`. Probamos hacer un `ping` hacia ellos y pudimos conectarnos:

![](/TP2/img/WhatsApp%20Image%202026-03-31%20at%2014.56.18.jpeg)
