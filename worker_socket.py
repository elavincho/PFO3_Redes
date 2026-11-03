# # (Servidor)

import socket
import threading
import json
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from werkzeug.security import generate_password_hash, check_password_hash

HOST = "127.0.0.1"
DB_NAME = "tareas.db"

# Diccionario para traducir los estados HTTP a texto
ESTADOS_HTTP = {
    200: "OK",
    201: "Created (Creado)",
    400: "Bad Request (Petición incorrecta)",
    401: "Unauthorized (No autorizado)",
    409: "Conflict (Conflicto)"
}

# Creamos el pool de hilos
pool = ThreadPoolExecutor(max_workers=5)

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena_hash TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            completada INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# --- LÓGICA DE NEGOCIO ---
def logica_registro(datos):
    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña")
    if not usuario or not contrasena:
        return {"status": 400, "error": "Faltan datos"}

    hash_pw = generate_password_hash(contrasena)
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)", (usuario, hash_pw))
        conn.commit()
        conn.close()
        return {"status": 201, "mensaje": f"Usuario '{usuario}' registrado"}
    except sqlite3.IntegrityError:
        return {"status": 409, "error": "El usuario ya existe"}

def logica_login(datos):
    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña")
    if not usuario or not contrasena:
        return {"status": 400, "error": "Faltan datos"}

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    fila = cur.fetchone()

    if fila is None or not check_password_hash(fila["contrasena_hash"], contrasena):
        conn.close()
        return {"status": 401, "error": "Credenciales inválidas"}

    # Crear tareas ficticias si no tiene
    cur.execute("SELECT COUNT(*) as c FROM tareas WHERE usuario_id = ?", (fila["id"],))
    if cur.fetchone()["c"] == 0:
        iniciales = ["Completar PFO 3", "Repasar hashing", "Probar sockets"]
        cur.executemany("INSERT INTO tareas (usuario_id, titulo) VALUES (?, ?)", [(fila["id"], t) for t in iniciales])
        conn.commit()

    cur.execute("SELECT * FROM tareas WHERE usuario_id = ?", (fila["id"],))
    tareas = [dict(row) for row in cur.fetchall()]
    conn.close()
    return {"status": 200, "mensaje": f"Bienvenido {usuario}", "tareas": tareas}

# --- MANEJO DE SOCKETS ---
def procesar_peticion(peticion_json, conn_cliente, puerto_worker):
    """Esta función corre dentro de un hilo del pool."""
    hilo_actual = threading.current_thread().name
    try:
        accion = peticion_json.get("accion")
        datos = peticion_json.get("datos", {})
        
        # 🔍 LOG: Mostramos qué petición llegó y qué hilo la tomó
        print(f"\n[Worker {puerto_worker}] 📥 Petición recibida: '{accion}' para usuario '{datos.get('usuario')}'")
        print(f"[Worker {puerto_worker}] 🧵 Procesando en el hilo: {hilo_actual}")

        # Simulamos un pequeño retraso para que se note la concurrencia
        time.sleep(1)

        if accion == "registro":
            respuesta = logica_registro(datos)
        elif accion == "login":
            respuesta = logica_login(datos)
        else:
            respuesta = {"status": 400, "error": "Acción no válida"}

        respuesta["worker"] = f"Worker en puerto {puerto_worker}"
        
        # 🔍 LOG: Mostramos el resultado antes de enviarlo con su descripción
        estado = respuesta.get("status")
        desc_estado = ESTADOS_HTTP.get(estado, "Desconocido")
        
        print(f"[Worker {puerto_worker}] ✅ Petición finalizada con estado {estado} ({desc_estado}). Enviando respuesta...")

        conn_cliente.sendall(json.dumps(respuesta).encode("utf-8"))
    except Exception as e:
        print(f"[Worker {puerto_worker}] ❌ Error: {e}")
        conn_cliente.sendall(json.dumps({"error": str(e)}).encode("utf-8"))
    finally:
        conn_cliente.close()

def atender_cliente(conn_cliente, puerto_worker):
    try:
        data = conn_cliente.recv(4096).decode("utf-8")
        if data:
            peticion_json = json.loads(data)
            # Enviamos al pool de hilos
            pool.submit(procesar_peticion, peticion_json, conn_cliente, puerto_worker)
    except Exception as e:
        print(f"[Worker {puerto_worker}] Error recibiendo datos: {e}")
        conn_cliente.close()

def iniciar_worker(puerto):
    init_db()
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, puerto))
    servidor.listen(5)
    
    print("="*60)
    print(f"🚀 WORKER INICIADO EN PUERTO {puerto}")
    print(f"🧵 Pool de hilos configurado con {pool._max_workers} workers concurrentes")
    print("="*60)
    print("Esperando peticiones...\n")

    while True:
        conn, addr = servidor.accept()
        # Hilo principal para manejar la conexión del socket
        threading.Thread(target=atender_cliente, args=(conn, puerto), daemon=True).start()

if __name__ == "__main__":
    import sys
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    iniciar_worker(puerto)
    
    