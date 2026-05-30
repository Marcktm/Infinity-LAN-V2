import socket
import threading
import json
from cryptography.fernet import Fernet, InvalidToken

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 1024

# Misma clave que usa el cliente
ENCRYPTION_KEY = b"DWWSd3HYDEE7TMzxnNqtUQXdgLjdTsyY9FYzXodkp5M="

def decrypt_payload(encrypted_payload: str, key: bytes) -> str:

    # Descrifra el payload cifrado con Fernet
    # Recibe el token Base64 como string, lo descifra y devuelve el texto plano

    f = Fernet(key)
    decrypted = f.decrypt(encrypted_payload.encode("utf-8"))
    return decrypted.decode("utf-8")


def handle_client(client_socket, client_address):
    ip_address = client_address[0]

    print(f"Hello {ip_address} welcome to the server!")

    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)

            if not data:
                break

            try:
                message = json.loads(data.decode("utf-8"))

                if (
                    isinstance(message, dict)
                    and "group" in message
                    and "payload" in message
                    and isinstance(message["group"], str)
                    and isinstance(message["payload"], str)
                ):
                    group = message["group"]
                    encrypted_payload = message["payload"]

                    # Mostramos lo que llegó cifrado
                    print(f"[CIFRADO]       {group}: {encrypted_payload[:60]}...")

                    # Intentamos descifrar el payload
                    try:
                        decrypted_payload = decrypt_payload(encrypted_payload, ENCRYPTION_KEY)
                        print(f"[DESCIFRADO]    {group}: {decrypted_payload}")
                    except InvalidToken:
                        print(f"[ERROR] No se pudo descifrar el mensaje de {group}. "
                              "¿Clave incorrecta o mensaje corrupto?")
                else:
                    print(f"{ip_address} wants to send an ill formatted message.")

            except json.JSONDecodeError:
                print(f"{ip_address} wants to send an ill formatted message.")

    except ConnectionResetError:
        pass

    finally:
        print(f"Bye {ip_address}!")
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )

            client_thread.start()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()