# Guía para agentes

## Arquitectura
- `api/app.py` contiene la API Flask y accede a MySQL mediante PyMySQL.
- `frontend/index.html` es una interfaz estática independiente que solicita `/api/tareas`.
- Consulta `.github/agents/app-respaldo-guide.agent.md` para análisis de configuración y puesta en marcha.

## Configuración y ejecución
- La API requiere que exista una base de datos MySQL y que estén definidas las variables `DB_HOST`, `DB_USER`, `DB_PASSWORD` y `DB_NAME`. `.env.example` contiene solo valores ficticios; no inventes credenciales reales ni las incluyas en el repositorio.
- Desde `api/`, instala dependencias con `python -m pip install -r requirements.txt` y ejecuta `python app.py` después de configurar esas variables. El servidor escucha en el puerto `5000`.
- La aplicación crea la tabla `tareas` al listar o crear tareas, pero no crea la base de datos.
- Para el entorno local con Docker, consulta `README.md`: copia `.env.example` a `.env`, cambia las contraseñas y ejecuta `docker compose up --build -d` desde la raíz. No borres el volumen `mysql_data` al detener los servicios.

## Validación y límites conocidos
- No se encontraron pruebas automatizadas. `docker compose config -q` valida la configuración y `docker compose build` construye las imágenes, pero ninguno sustituye pruebas de la aplicación.
- Nginx sirve el frontend y reenvía `/api/` a Flask bajo el mismo origen. No des por hecho que abrir `frontend/index.html` directamente conectará con la API.