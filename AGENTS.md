# Guía para agentes

## Arquitectura
- `api/app.py` contiene la API Flask y accede a MySQL mediante PyMySQL.
- `frontend/index.html` es una interfaz estática independiente que solicita `/api/tareas`.
- Consulta `.github/agents/app-respaldo-guide.agent.md` para análisis de configuración y puesta en marcha.

## Configuración y ejecución
- La API requiere que exista una base de datos MySQL y que estén definidas las variables `DB_HOST`, `DB_USER`, `DB_PASSWORD` y `DB_NAME`. No hay un archivo de configuración de ejemplo; no inventes valores ni incluyas credenciales reales en el repositorio.
- Desde `api/`, instala dependencias con `python -m pip install -r requirements.txt` y ejecuta `python app.py` después de configurar esas variables. El servidor escucha en el puerto `5000`.
- La aplicación crea la tabla `tareas` al listar o crear tareas, pero no crea la base de datos.

## Validación y límites conocidos
- No se encontraron pruebas automatizadas ni comandos de build configurados. No afirmes que las pruebas pasan si no existen o no se ejecutaron.
- El frontend usa rutas relativas y Flask no sirve actualmente el HTML. Para que la interfaz llegue a la API, sirve ambos bajo el mismo origen o configura un proxy; no des por hecho que abrir el HTML directamente funcionará.