# App Respaldo

Aplicacion de tareas con una API Flask, una interfaz estatica y MySQL. El entorno local usa Docker Compose; Nginx sirve la interfaz y reenvia `/api/` a la API para mantener un unico origen.

## Requisitos

- Docker Desktop con Docker Compose v2.

## Iniciar localmente

Desde la raiz del repositorio, en PowerShell:

```powershell
Copy-Item .env.example .env
```

Antes del primer arranque, edita `.env` y reemplaza las contrasenas de ejemplo. MySQL inicializa la base de datos y el usuario al crear por primera vez el volumen `mysql_data`; cambiar despues las variables no cambia las credenciales ya guardadas en MySQL. Si el volumen ya existe, conserva sus credenciales o actualiza la cuenta de forma deliberada. No borres el volumen para resolver un problema de credenciales si necesitas conservar los datos.

Luego ejecuta:

```powershell
docker compose config -q
docker compose up --build -d
docker compose ps
```

Abre `http://localhost:8080`. La API y MySQL no publican puertos al host; Compose las conecta en una red interna. MySQL conserva los datos en el volumen `mysql_data`.

Para consultar los logs o detener los contenedores:

```powershell
docker compose logs -f
docker compose down
```

`docker compose down` conserva los datos. No uses `docker compose down -v` salvo que quieras borrar permanentemente el volumen de MySQL.

## Alcance

Esta configuracion esta destinada al desarrollo local. La API se ejecuta con el servidor integrado de Flask; antes de desplegar en produccion, usa un servidor WSGI, gestiona secretos con un mecanismo apropiado y revisa TLS, imagenes y politicas de red. El repositorio aun no contiene pruebas automatizadas.