import socket
import json
import argparse
from cryptography.fernet import Fernet

# En un sistema real, NUNCA se hardcodea la clave en el código.
# Se usaría un archivo de configuración, variable de entorno, o un key server.
ENCRYPTION_KEY = b"DWWSd3HYDEE7TMzxnNqtUQXdgLjdTsyY9FYzXodkp5M="

def main():
    # Configuración de IP y puerto
    # Si no se pasan argumentos se usa los valores por defecto
    parser = argparse.ArgumentParser(description="Cliente TCP para enviar mensajes JSON")
    parser.add_argument("--host", type=str, default="127.0.0.1",
                        help="IP del servidor (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000,
                        help="Puerto del servidor (default: 5000)")
    parser.add_argument("--group", type=str, default=None,
                        help="Nombre del grupo (si no se pasa, se pregunta al inicio)")
    args = parser.parse_args()

    host = args.host
    port = args.port

    # Si no se paso el nombre del gupo se le pide al usuario que lo intgrrese
    if args.group:
        group = args.group
    else:
        group = input("Ingresá el nombre de tu grupo: ")

    # Conexion al servidor
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))
        print(f"Conectado al servidor {host}:{port}")
        print("Escribí mensajes para enviar. Escribí 'salir' para desconectarte.\n")
    except ConnectionRefusedError:
        print(f"No se pudo conectar a {host}:{port}. ¿Está corriendo el servidor?")
        return
    except Exception as e:
        print(f"Error al conectar: {e}")
        return

    # Loop interactivo de envío
    try:
        while True:
            # Leemos el mensaje del usuario por consola
            payload = input(">> ")

            # Desconectado si el usuario escribe "salir"
            if payload.lower() == "salir":
                print("Desconectando...")
                break

            # Si el usuario no escribió nada, no enviamos
            if not payload:
                continue

            # Serializamos en el formato que espera el servidor
            message = {
                "group": group,
                "payload": payload
            }

            # json.dumps() convierte el diccionario a un string JSON
            # .encode("utf-8") convierte el string a bytes para enviar por el socket
            json_data = json.dumps(message)
            client.sendall(json_data.encode("utf-8"))

            print(f"   [Enviado] {json_data}")

    except KeyboardInterrupt:
        print("\nDesconectando (Ctrl+C)...")
    except BrokenPipeError:
        print("El servidor cerró la conexión.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Conexión cerrada.")


if __name__ == "__main__":
    main()