# Interfaz web de demostración

1. Abrir terminal en la raíz del proyecto.
2. Ejecutar `python scripts/crear_base.py` (solo si no existe `db/colorink_demo.sqlite`).
3. Ejecutar `python prototipo_web/servidor.py`.
4. Abrir `http://127.0.0.1:8765`.

El servidor escucha solo en el equipo local y utiliza la base SQLite de demostración. Las lecturas QR se simulan escribiendo o ingresando con un lector tipo teclado el código de la bobina. No existe autenticación; no utilizar en producción ni exponer por Internet. Para reiniciar el escenario eliminar el archivo `db/colorink_demo.sqlite` generado y ejecutar nuevamente el comando de creación.
