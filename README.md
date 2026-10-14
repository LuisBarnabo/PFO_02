# Sistema de Gestión de Tareas y Usuarios (Cliente-Servidor)

Este proyecto es una aplicación de gestión de usuarios y tareas desarrollada con **Python**, **Flask**, **SQLite** y una arquitectura de tipo **Cliente-Servidor**. 

El sistema consta de un **Servidor** que procesa la lógica, la seguridad y los datos, y un **Cliente de Consola** interactivo que permite al usuario gestionar sus cuentas y tareas, además de contar con una vista web sincronizada renderizada en HTML.

---

## Tecnologías utilizadas
* **Python 3** (Lenguaje principal de programación).
* **Flask** (Framework para crear el servidor web y la API REST).
* **SQLite3** (Base de datos relacional embebida).
* **Werkzeug Security** (Librería para el hasheo seguro de contraseñas mediante PBKDF2).
* **Requests** (Librería para la comunicación HTTP entre el cliente y el servidor).

---

## Estructura del Proyecto
```text
pfo-gestion-tareas/
│
├── servidor.py          # Servidor central, base de datos y endpoints API
├── cliente.py           # Aplicación interactiva de consola para el usuario
├── manual_usuario.pdf   # Manual de usuario detallado con capturas de pantalla
├── templates/
│   └── tareas.html      # Plantilla web para visualizar tareas en el navegador
└── README.md            # Documentación principal del repositorio
```
---

## Guía de Instalación y Ejecución (Paso a Paso)
Paso 1: Requisitos previos
Asegúrate de tener instalado Python en tu computadora. Puedes verificarlo abriendo tu terminal y ejecutando:
`python --version`

Paso 2: Instalar las dependencias necesarias
El servidor y el cliente requieren dos librerías externas (`Flask` y `Requests`). Instálalas ejecutando el siguiente comando en tu terminal:

`pip install flask requests`

Paso 3: Encender el Servidor
El servidor es el núcleo del sistema y debe permanecer activo durante toda la sesión.

1. Abre una ventana de la terminal.
2. Dirígete a la carpeta del proyecto.
3. Ejecuta el servidor: `python servidor.py`
(Deberás ver un mensaje indicando que corre en `http://127.0.0.1:5000`). Deja esta terminal abierta.

Paso 4: Ejecutar el Cliente

1. Abre una SEGUNDA ventana de la terminal (dejando la del servidor corriendo en la primera).
2. Dirígete a la misma carpeta del proyecto.
3. Ejecuta la interfaz de cliente: `python cliente.py`

---

## Funcionalidades del Sistema
Una vez en el menú principal del cliente (`cliente.py`), podrás operar con las siguientes opciones:

1. **Registrar nuevo usuario**: Permite dar de alta un usuario validando contraseñas duplicadas en bucle, evitando campos vacíos y ofreciendo la opción de cancelar (`salir`) en cualquier momento. Las credenciales se almacenan con hashing seguro.

2. **Iniciar sesión**: Valida las credenciales contra la base de datos y otorga acceso al panel de gestión privado del usuario activo.

3. **Panel de Gestión de Tareas**:

  * Ver mis tareas: Lista en consola todas las tareas creadas por el usuario autenticado.
  * Crear nueva tarea: Permite registrar un título y una descripción opcional, con confirmación de guardado.
  * Ver vista web (HTML): Abre automáticamente tu navegador predeterminado mostrando un panel web moderno con la tabla sincronizada de tus tareas `(http://127.0.0.1:5000/tareas?usuario=...)`.
  * Cerrar sesión / Salir: Permite volver al menú principal de forma segura.

---

## Documentación adicional:
Puedes consultar el Manual de Usuario completo en PDF con todas las capturas de pantalla detalladas en el archivo **manual_usuario.pdf** incluido en este repositorio.