# (Simula Nginx)
import socket
import threading

HOST = "127.0.0.1"
PORT_BALANCEADOR = 8080
WORKERS = [("127.0.0.1", 5001), ("127.0.0.1", 5002)] 

indice = 0
lock = threading.Lock()

def obtener_worker():
    global indice
    with lock:
        worker = WORKERS[indice]
        indice = (indice + 1) % len(WORKERS)
        return worker

def manejar_cliente(conn_cliente):
    try:
        # Recibimos los datos del cliente
        datos = conn_cliente.recv(4096)
        if not datos:
            return

        worker_host, worker_port = obtener_worker()
        print(f"[Balanceador] Redirigiendo petición a puerto {worker_port}")

        # Nos conectamos al worker
        conn_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_worker.connect((worker_host, worker_port))
        conn_worker.sendall(datos)

        # Esperamos respuesta del worker y la devolvemos
        respuesta = conn_worker.recv(4096)
        conn_cliente.sendall(respuesta)
        
        conn_worker.close()
    except Exception as e:
        conn_cliente.sendall(f'{{"error": "Error en balanceador: {e}"}}'.encode("utf-8"))
    finally:
        conn_cliente.close()

def iniciar_balanceador():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT_BALANCEADOR))
    servidor.listen(10)
    print(f"⚖️ Balanceador escuchando en {HOST}:{PORT_BALANCEADOR}")

    while True:
        conn, addr = servidor.accept()
        threading.Thread(target=manejar_cliente, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    iniciar_balanceador()