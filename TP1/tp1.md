# Parte 1: Simulación de envío de paquetes, ARP y ruteo entre redes

## 1. Identificación de dispositivos y armado de la topología
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
