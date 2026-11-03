<img src="https://i.ibb.co/VYkx7wHV/ifts29-Logo.png" width="80" height="80" alt="ifts-29"/>

# Programación sobre Redes

## Práctica Formativa Obligatoria 2

## Sistema de Gestión de Tareas con API y Base de Datos

API REST desarrollada con **Flask** y **SQLite** para registrar usuarios, iniciar
sesión y consultar tareas.

---

## Instalación

```bash
git clone https://github.com/elavincho/PFO2_Redes.git
cd PFO2_Redes
python -m venv venv
```
## Activar el entorno virtual:

```bash
Windows (PowerShell): .\venv\Scripts\Activate.ps1
```

```bash
Windows (CMD): venv\Scripts\activate.bat
```

```bash
macOS / Linux: source venv/bin/activate
```

## Instalar depencencias:

```bash
pip install flask requests
```

## Ejecución

  **1. Levantar el servidor:**

```bash
python servidor.py
```

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/servidor_consola.png" width="" height="" alt="servidor_consola"/>

  - El Servidor se inicia en http://127.0.0.1:5000.

  **2. En otra terminal (con el venv activado), ejecutar el cliente:**

```bash
python cliente.py
```

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/cliente_consola.png" width="" height="" alt="cliente_consola"/>


## Endpoints

### ▶️ Registro por Consola

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/registro_consola.png" width="" height="" alt="registro_consola"/>

### ▶️ Registro en el Navegador

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/registro_web.png" width="" height="" alt="registro_web"/>

### ▶️ Login por Consola

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/iniciar_sesion_consola.png" width="" height="" alt="login_consola"/>

### ▶️ Login en el Navegador

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/login_web.png" width="" height="" alt="login_web"/>

### ▶️ Tareas por Consola

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/tareas_consola.png" width="" height="" alt="login_consola"/>

### ▶️ Tareas en el Navegador

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/tareas_web.png" width="" height="" alt="tareas_web"/>

### ▶️ Logout en el Navegador

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/logout_web.png" width="" height="" alt="logout_web"/>


## Estructura del proyecto
```bash
pfo2-tareas/
├── servidor.py        # API Flask + SQLite
├── cliente.py         # Cliente de consola
├── tareas.db          # Base de datos (se genera automáticamente)
└── README.md
```

## 📋 Respuestas conceptuales

### ✅ ¿Por qué hashear contraseñas?

Hashear las contraseñas es una práctica fundamental de seguridad al construir cualquier sistema que gestione credenciales. Las razones principales son:

**Evita almacenar datos sensibles en texto plano.**
Si la base de datos es robada, filtrada o mal compartida, un atacante no
obtiene las contraseñas reales de los usuarios. Solo ve cadenas de hash
ilegibles e irreversibles.

**Protege a los usuarios que reutilizan contraseñas.**
Muchas personas usan la misma contraseña para el correo, el banco o redes
sociales. Si un sistema la guarda en texto plano y se filtra, compromete
todos los demás servicios del usuario.

**El hash es una función unidireccional.**
A diferencia del cifrado (que se puede descifrar con una clave), un hash
no se puede revertir matemáticamente. No existe forma práctica de
obtener la contraseña original a partir del hash.

**Uso automático de salt.**
Librerías como Werkzeug (generate_password_hash) aplican un salt
aleatorio a cada contraseña antes de hashearla. Esto significa que dos
usuarios con la misma contraseña obtienen hashes completamente distintos,
lo que impide ataques de tablas precalculadas (rainbow tables).

**Verificación sin conocer la contraseña.**
El servidor nunca necesita "saber" la contraseña original. Solo compara el
hash recién calculado con el almacenado usando check_password_hash(). La
contraseña real nunca toca el disco ni la base de datos.

**Cumplimiento normativo.**
Regulaciones como GDPR (Europa) o Ley de Protección de Datos
Personales (Argentina) exigen medidas de seguridad razonables para datos
sensibles, y el hasheo de contraseñas es una de ellas.

**Conclusión:** hashear contraseñas no es opcional, es un requisito mínimo
de cualquier sistema que se tome en serio la seguridad de sus usuarios.

## ✅ Ventajas de usar SQLite en este proyecto

SQLite es una base de datos embebida, sin servidor, que se guarda en un
único archivo. Para un PFO como este, ofrece ventajas claras:

**Cero configuración.**
No hace falta instalar, administrar ni levantar un servidor de base de
datos (como MySQL o PostgreSQL). Simplemente se usa el módulo sqlite3 que
ya viene incluido en Python.

**Portabilidad total.**
Toda la base de datos es un solo archivo (tareas.db). Se puede
copiar, mover, respaldar o versionar fácilmente entre equipos.

**Ideal para desarrollo, prototipado y proyectos pequeños.**
Para un sistema de tareas con pocos usuarios concurrentes, SQLite es más
que suficiente y evita la sobrecarga de un motor cliente-servidor.

**Sin dependencias externas.**
No requiere instalar controladores, ni configurar usuarios, puertos o
permisos del motor. Todo funciona "out of the box".

**Soporta SQL estándar.**
Permite JOIN, claves foráneas, UNIQUE, transacciones, AUTOINCREMENT,
etc. Lo que aprendes con SQLite es directamente aplicable a otros motores.

**Rápida para lecturas.**
Al ser un archivo local, las lecturas son muy veloces y sin latencia de red.

**Integración nativa con Python.**
El módulo sqlite3 viene en la biblioteca estándar, así que el código es
simple, limpio y sin capas extra.

**Limitación a tener en cuenta:** SQLite no está pensado para alta
concurrencia de escritura. Si el proyecto creciera a cientos de usuarios
simultáneos escribiendo, convendría migrar a PostgreSQL o MySQL. Para un PFO
académico, es la elección ideal.

##  Capturas de pantalla

### ▶️ Credenciales Invalidas

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/credenciales_invalidas_consola.png" width="" height="" alt="registro_consola"/>

### ▶️ Peticiones al Servidor

<img src="https://github.com/elavincho/PFO2_Redes/blob/master/img/servidor_consola_2.png" width="" height="" alt="registro_consola"/>




<img src="https://i.ibb.co/VYkx7wHV/ifts29-Logo.png" width="40" height="40" alt="ifts-29"/>

#### Programación sobre Redes
