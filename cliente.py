import requests, getpass, webbrowser


URL_BASE = "http://127.0.0.1:5000"

def menu_usuario_logueado(usuario_activo):
    """Menú secundario exclusivo para el usuario que ya inició sesión."""
    while True:
        print("\n=====================================================")
        print(f"--- PANEL DE GESTIÓN --- (Usuario: {usuario_activo}) ---")
        print("=====================================================")
        print("1. Ver mis tareas")
        print("2. Crear nueva tarea")
        print("3. Ver vista web de bienvenida (HTML)")
        print("4. Cerrar sesión")

        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            listar_mis_tareas(usuario_activo)
        elif opcion == "2":
            crear_nueva_tarea(usuario_activo)
        elif opcion == "3":
            ver_vista_html(usuario_activo)
        elif opcion == "4":
            print("Cerrando sesión...")
            break
        else:
            print("[Error] Opción no válida.")

def listar_mis_tareas(usuario):
    try:
        response = requests.get(f"{URL_BASE}/tareas/{usuario}")
        if response.status_code == 200:
            tareas = response.json()
            print("\n====================================")
            print(f"--- TAREAS DE {usuario.upper()} ---")
            print("====================================")
            if not tareas:
                print("No tienes tareas registradas.")
                return
            for t in tareas:
                print(f"[{t['id']}] {t['titulo']} - Estado: {t['estado']}")
                if t['descripcion']:
                    print(f"    Descripción: {t['descripcion']}")
        else:
            print("[Error] No se pudieron recuperar las tareas.")
    except Exception as e:
        print(f"[Error de conexión] {e}")

def crear_nueva_tarea(usuario):
    print("\n===================")
    print("--- NUEVA TAREA ---")
    print("===================")
    titulo = input("Título de la tarea: ").strip()
    descripcion = input("Descripción (opcional): ").strip()

    if not titulo:
        print("[Error] El título es obligatorio.")
        return

    # Confirmación final antes de enviar al servidor
    confirmacion = input(f"¿Confirma crear la tarea '{titulo}'? (s/n): ").strip().lower()
    if confirmacion != 's':
        print("[Cancelado] La creación de la tarea fue descartada.")
        return

    datos = {
        "usuario": usuario,
        "titulo": titulo,
        "descripcion": descripcion
    }

    try:
        response = requests.post(f"{URL_BASE}/tareas", json=datos)
        resultado = response.json()
        if response.status_code == 201:
            print(f"[Éxito] {resultado.get('mensaje')}")
        else:
            print(f"[Error] {resultado.get('error')}")
    except Exception as e:
        print(f"[Error de conexión] {e}")

def ver_vista_html(usuario_activo):
    url_objetivo = f"{URL_BASE}/tareas?usuario={usuario_activo}"
    print(f"\n[Servidor] Abriendo panel web para '{usuario_activo}': {url_objetivo}")
    try:
        webbrowser.open(url_objetivo)

        response = requests.get(url_objetivo)
        if response.status_code == 200:
            print(f"Estado HTTP: {response.status_code} OK (HTML renderizado con éxito)")
        else:
            print(f"No se pudo acceder. Código: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def registrar_usuario():
    print("\n===========================")
    print("--- REGISTRO DE USUARIO ---")
    print("===========================")
    print("(Escribe 'salir' en cualquier momento para cancelar)")
    
    usuario = input("Ingrese nombre de usuario: ").strip()
    if usuario.lower() == 'salir':
        print("[Cancelado] Operación abortada.")
        return

    if not usuario:
            print("[Error] El usuario no puede estar vacío.")
            return

    while True:

        clave = getpass.getpass("Ingrese contraseña: ").strip()
        if clave.lower() == 'salir':
            print("[Cancelado] Operación abortada.")
            return

        # Comprobación de contraseña repetida
        clave_confirmacion = getpass.getpass("Reingrese la contraseña: ").strip()
        if clave_confirmacion.lower() == 'salir':
            print("[Cancelado] Operación abortada.")
            return

        if not clave:
            print("[Error] La contraseña no puede estar vacía.")
            continue

        if clave == clave_confirmacion:
            break
        else:
            print("[Error] Las contraseñas no coinciden. Intente de nuevo.\n")

    # Confirmación final antes de enviar al servidor
    confirmacion = input(f"¿Confirma dar de alta al usuario '{usuario}'? (s/n): ").strip().lower()
    if confirmacion != 's':
        print("[Cancelado] El registro fue descartado.")
        return

    datos = {
        "usuario" : usuario,
        "contraseña": clave
    }

    try: 
        # Peticion POST al endpoint de registro
        response = requests.post(f"{URL_BASE}/registro", json=datos)
        resultado = response.json()

        if response.status_code == 201:
            print(f"[Éxito] {resultado.get('mensaje')}")
        else:
            print(f"[Error {response.status_code}] {resultado.get('error')}")

    except requests.exceptions.ConnectionError:
        print("[Error] No se pudo conectar al servidor. Asegúrate de que 'servidor.py' esté encendido.")
    except Exception as e:
        print(f"[Error inesperado] {e}")

def iniciar_sesion():
    print("\n========================")
    print("--- INICIO DE SESIÓN ---")
    print("========================")
    usuario = input("Ingrese nombre de usuario: ").strip()
    clave = getpass.getpass("Ingrese contraseña: ").strip()

    if not usuario or not clave:
        print("[Error] Debe completar ambos campos.")
        return

    datos = {
        "usuario": usuario,
        "contraseña": clave
    }

    try:
        # Petición POST al endpoint de login
        response = requests.post(f"{URL_BASE}/login", json=datos)
        resultado = response.json()

        if response.status_code == 200:
            print(f"\n[Éxito] {resultado.get('mensaje')}")
            # Si el login es exitoso, permitimos consultar el endpoint protegido de tareas
            menu_usuario_logueado(usuario)
        else:
            print(f"[Error {response.status_code}] {resultado.get('error')}")

    except requests.exceptions.ConnectionError:
        print("[Error] No se pudo conectar al servidor. Asegúrate de que 'servidor.py' esté encendido.")
    except Exception as e:
        print(f"[Error inesperado] {e}")

def consultar_tareas():
    # Pregunta si desea acceder al html de bienvenida
    opcion = input("\n¿Desea acceder al panel de tareas (GET /tareas)? (s/n): ").strip().lower()
    if opcion == 's':
        try:
            response = requests.get(f"{URL_BASE}/tareas")
            if response.status_code == 200:
                print("\n[Respuesta del Servidor - /tareas]")
                print("Acceso exitoso. El servidor devolvió la vista HTML de bienvenida.")
                print(f"Código HTTP: {response.status_code} OK")
            else:
                print(f"No se pudo acceder. Código: {response.status_code}")
        except Exception as e:
            print(f"Error al consultar tareas: {e}")

def menu_principal():
    while True:
        print("\n===============================")
        print("  SISTEMA DE GESTIÓN (CLIENTE)  ")
        print("===============================")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        
        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            print("Saliendo del cliente. ¡Hasta luego!")
            break
        else:
            print("[Error] Opción no válida. Intente de nuevo con 1, 2 o 3.")

if __name__ == "__main__":
    menu_principal()