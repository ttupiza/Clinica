# Proyecto de Registro y Gestión de Citas

Este proyecto es una aplicación web desarrollada con Flask para el registro de usuarios (doctores y pacientes) y la gestión de citas médicas.

## Requisitos previos

- Python 3.7 o superior instalado en tu sistema.
- Instalar las dependencias necesarias ejecutando:
  ```bash
  pip install -r requirements.txt
  ```

## Pasos para iniciar el proyecto

1. Asegúrate de estar en el directorio raíz del proyecto:
   ```bash
   cd /Users/kuro/Development/Clinica-1
   ```

2. Ejecuta el archivo principal `app.py`:
   ```bash
   python app.py
   ```

3. Accede a la aplicación en tu navegador en la dirección:
   ```
   http://127.0.0.1:5000
   ```

## Notas adicionales

- Asegúrate de que el archivo `database.db` esté configurado correctamente y que la base de datos haya sido inicializada.
- Si necesitas reiniciar la base de datos, utiliza la función `initialize_database()` incluida en el proyecto.

¡Disfruta usando la aplicación!