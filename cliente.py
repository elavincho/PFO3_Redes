# (Cliente con sockets)

import socket
import json

HOST = "127.0.0.1"
PORT = 8080

def enviar_peticion(accion, datos):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
        
        peticion = {"accion": accion, "datos": datos}
        cliente.sendall(json.dumps(peticion).encode("utf-8"))
        
        respuesta = cliente.recv(4096).decode("utf-8")
        cliente.close()
        return json.loads(respuesta)
    except ConnectionRefusedError:
        print("\n❌ Error: El balanceador no está corriendo.")
        return None

def registrar():
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    res = enviar_peticion("registro", {"usuario": usuario, "contraseña": contrasena})
    if res:
        print(f"[{res.get('status')}] {res.get('mensaje') or res.get('error')}")

def login():
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    res = enviar_peticion("login", {"usuario": usuario, "contraseña": contrasena})
    if res:
        if res.get("status") == 200:
            print(f"\n✅ {res['mensaje']} (Atendido por: {res['worker']})")
            print("📋 Tus tareas:")
            for t in res["tareas"]:
                print(f" - {t['titulo']}")
        else:
            print(f"❌ [{res.get('status')}] {res.get('error')}")

def main():
    while True:
        print("\n=== GESTOR DE TAREAS (Distribuido) ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        op = input("Opción: ").strip()

        if op == "1":
            registrar()
        elif op == "2":
            login()
        elif op == "3":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()