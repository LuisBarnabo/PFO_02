from flask import Flask, request, jsonify, render_template
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = "usuarios.db"

def inicializar_bd():
    """Configura y crea la tabla de usuarios y tareas en SQLite si no existe."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Tabla de Usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    clave TEXT NOT NULL
                )
            ''')

            # Tabla de Tareas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tareas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL,
                    titulo TEXT NOT NULL,
                    descripcion TEXT,
                    estado TEXT DEFAULT 'pendiente'
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"[Error BD] No se pudo inicializar la base de datos: {e}")

# Endpoint de Registro
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    datos = request.get_json()

    usuario = datos.get("usuario")
    clave = datos.get("contraseña")

    if not usuario or not clave:
        return jsonify({"error": "Faltan datos obligatorios (usuario o contraseña)"})

    # Hashear la contraseña antes de guardarla
    clave_hash = generate_password_hash(clave)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (usuario, clave) VALUES (?, ?)",
                (usuario, clave_hash)
            )
            conn.commit()
        return jsonify({"mensaje": f"Usuario '{usuario}' registrado con éxito."}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "El nombre de usuario ya está en uso."}), 409
    except sqlite3.Error as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

# Endpoint de Login
@app.route('/login', methods=['POST'])
def login_usuario():
    datos = request.get_json()

    usuario = datos.get("usuario")
    clave = datos.get("contraseña")

    if not usuario or not clave:
        return jsonify({"error": "Credenciales incompletas"}), 400

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT clave FROM usuarios WHERE usuario = ?", (usuario,))
            resultado = cursor.fetchone()

        # Si el usuario no existe o la contraseña no coincide
        if not resultado or not check_password_hash(resultado[0], clave):
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        return jsonify({"mensaje": f"Bienvenido de nuevo, {usuario}"}), 200

    except sqlite3.Error as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500

# Endpoint de Tareas 
"""Muestra el html de bienvenida"""
@app.route('/tareas', methods=['GET'])
def ver_tareas_html():
    """Endpoint que renderiza el HTML y opcionalmente carga las tareas si recibe un usuario por query param."""
    usuario = request.args.get('usuario')
    tareas = []

    if usuario:
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, titulo, descripcion, estado FROM tareas WHERE usuario = ?", (usuario,))
                filas = cursor.fetchall()

                for fila in filas:
                    tareas.append({
                        "id": fila[0],
                        "titulo": fila[1],
                        "descripcion": fila[2],
                        "estado": fila[3]
                    })

        except sqlite3.Error as e:
            print(f"[Error BD] {e}")

    return render_template('tareas.html', usuario=usuario, tareas=tareas)

@app.route('/tareas', methods=['POST'])
def crear_tarea():
    # Endpoint para que el usuario cree una tarea
    datos = request.get_json()
    usuario = datos.get("usuario")
    titulo = datos.get("titulo")
    descripcion = datos.get("descripcion", "")
    if not usuario or not titulo:
        return jsonify({"error": "Se requiere usuario y titulo de tarea"}), 400

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            # 1. VALIDACIÓN: Comprobar si el usuario realmente existe en la BD
            cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
            usuario_existe = cursor.fetchone()
            
            if not usuario_existe:
                return jsonify({"error": f"El usuario '{usuario}' no existe. Debe registrarse primero."}), 404

            # 2. Si el usuario existe, procedemos a insertar la tarea
            cursor.execute(
                "INSERT INTO tareas (usuario, titulo, descripcion) VALUES (?, ?, ?)",
                (usuario, titulo, descripcion)
            )
            conn.commit()
        return jsonify({"mensaje": "Tarea creada exitosamente."}), 201
    except sqlite3.Error as e:
        return jsonify({"error": f"Error al guardar tarea: {e}"}), 500

@app.route('/tareas/<usuario>', methods=['GET'])
def listar_tareas(usuario):
    """Endpoint para listar todas las tareas de un usuario especifico."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, titulo, descripcion, estado FROM tareas WHERE usuario = ?", (usuario,))
            filas = cursor.fetchall()

            tareas = []
            for fila in filas:
                tareas.append({
                    "id": fila[0],
                    "titulo": fila[1],
                    "descripcion": fila[2],
                    "estado": fila[3]
                })

        return jsonify(tareas), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Error al obtener tareas: {e}"}), 500

if __name__ == '__main__':
    #Inicializamos la base de datos al arrancar el script
    inicializar_bd()
    # Ejecutamos el servidor Flask en modo desarrollo en el puerto 5000
    app.run(debug=True, port=5000)