---
name: dockerizacion-apps
description: 'Úsala para dockerizar aplicaciones existentes o nuevas, diseñar Dockerfiles e imágenes seguras, crear Docker Compose, conectar servicios y datos persistentes, o revisar una configuración Docker. Sigue un flujo de inspección, diseño, implementación y validación.'
user-invocable: true
---

# Dockerización de aplicaciones

Especialízate en convertir aplicaciones en contenedores reproducibles, mantenibles y seguros. Inspecciona primero el repositorio y sus restricciones. Adapta la solución al stack real; no fuerces una plantilla universal ni cambies la lógica de la aplicación si la infraestructura puede resolver el problema.

## Cuándo usarla

- Crear o revisar un `Dockerfile`, `.dockerignore` o configuración de Docker Compose.
- Contenerizar una aplicación existente o preparar su ejecución local mediante contenedores.
- Conectar API, frontend, base de datos, caché u otros servicios.
- Diagnosticar fallos de build, inicio, red, persistencia o despliegue en Docker.

## Principios

- Separa desarrollo local y producción cuando tengan requisitos distintos; confirma el objetivo si no está claro.
- Basa decisiones en código, manifiestos, documentación y configuración existentes. Expón las incertidumbres antes de elegir arquitectura.
- Usa imágenes base oficiales, versiones explícitas y el menor conjunto de paquetes necesario. No uses `latest` como estrategia de versionado.
- Ejecuta la aplicación como usuario sin privilegios; usa el formato exec en `ENTRYPOINT` y `CMD` para que reciba correctamente señales y cierre.
- Mantén secretos fuera de imágenes, argumentos de build, repositorio y logs. Usa variables de entorno para desarrollo local y mecanismos de secretos adecuados en producción.
- Limita puertos publicados, permisos, capacidades y acceso a datos a lo necesario. No expongas bases de datos al host por defecto.
- No borres volúmenes ni datos. Nunca ejecutes `docker compose down -v`, `docker volume rm` ni acciones equivalentes sin autorización explícita.
- No afirmes que una imagen, servicio o prueba funciona si no se ejecutó y verificó.

## Flujo de trabajo

1. **Inspeccionar el proyecto**
   - Lee las instrucciones del repositorio, documentación, manifiestos de dependencias, puntos de entrada y configuración existente.
   - Identifica stack, comandos de inicio, puertos, servicios externos, archivos estáticos, almacenamiento persistente y requisitos de compilación.
   - Busca archivos Docker existentes, tests, secretos accidentales y convenciones de despliegue. No muestres ni copies secretos encontrados.
   - Comprueba si Docker y Compose están disponibles cuando debas validar; si no lo están, continúa con revisiones estáticas y declara esa limitación.

2. **Definir la arquitectura**
   - Distingue qué procesos necesitan contenedores separados y cuáles son servicios administrados externos.
   - Para varios servicios locales, considera Compose, red interna y nombres de servicio como DNS. Dentro de un contenedor, `localhost` apunta a ese contenedor, no a otro servicio.
   - Diseña explícitamente el flujo del navegador hacia el frontend y la API, incluyendo proxy y origen cuando corresponda.
   - Decide cómo se conservan datos, cómo se comprueba la disponibilidad y cómo se inician dependencias. No confundas orden de inicio con preparación del servicio.
   - Antes de implementar decisiones con impacto (desarrollo frente a producción, topología, almacenamiento o publicación de puertos), pregunta si el contexto no las determina.

3. **Elegir los archivos necesarios**
   - Añade solo los artefactos requeridos: `Dockerfile`, `.dockerignore`, `compose.yaml` o `compose.yml`, y opcionalmente configuración de proxy, scripts de inicialización o `.env.example`.
   - No crees a la vez variantes redundantes de Compose ni múltiples Dockerfiles sin una necesidad concreta.
   - Si se requiere `.env`, verifica o actualiza `.gitignore` para excluirlo. El ejemplo solo contiene nombres y valores ficticios; nunca escribas credenciales reales.
   - Mantén instrucciones de ejecución concisas y enlaza documentación existente en vez de duplicarla.

4. **Construir imágenes seguras y reproducibles**
   - Ordena las capas para aprovechar caché: copia primero manifiestos de dependencias, instala y copia luego el código.
   - Usa builds multi-stage cuando separen herramientas de compilación del runtime o reduzcan significativamente la imagen; no los añadas por rutina.
   - Excluye del contexto con `.dockerignore` entornos virtuales, cachés, control de versiones, secretos, builds locales y dependencias que se instalan dentro de la imagen.
   - No copies archivos secretos. No uses `ARG` o `ENV` de Docker para incorporar secretos durante el build.
   - Evita procesos como root, instalaciones innecesarias, `privileged`, montajes del socket Docker y permisos amplios.
   - Incluye `HEALTHCHECK` solo cuando haya una comprobación fiable y compatible con el runtime. No añadas herramientas de diagnóstico innecesarias a producción.

5. **Configurar servicios y persistencia**
   - Usa variables de entorno para configuración. En Compose, los servicios se comunican por el nombre del servicio y el puerto interno del contenedor.
   - Publica al host solo los servicios que deban ser accesibles desde fuera de la red Docker. La API y la base de datos pueden permanecer internas si un proxy es el único punto de entrada.
   - Usa volúmenes nombrados para datos que deban persistir; identifica claramente cualquier bind mount destinado solo al desarrollo.
   - Añade healthchecks realistas. Usa condiciones de disponibilidad en `depends_on` solo si el healthcheck del servicio dependiente representa readiness.
   - Configura reinicio, migraciones e inicialización de datos solo según las necesidades verificadas. No presupongas que una imagen de base de datos crea la base, el usuario o el esquema requerido por la aplicación.

6. **Validar por etapas**
   - Revisa estáticamente rutas, contextos de build, puertos, nombres de servicio, interpolación de variables, persistencia y exclusiones de `.dockerignore`.
   - Si Compose está disponible, valida primero con `docker compose config -q` y luego construye con `docker compose build`.
   - Inicia solo los servicios solicitados o necesarios para la validación. Revisa `docker compose ps`, logs, estado de healthchecks y una petición funcional apropiada.
   - Comprueba persistencia tras recrear el contenedor solo si es seguro y no implica borrar datos existentes.
   - Ejecuta tests del proyecto y análisis de imagen si existen y están disponibles. No sustituyas los tests por un build exitoso.
   - Si algo falla, usa el error observado para corregir la causa y repite la validación enfocada. No limpies volúmenes como solución genérica.

7. **Entregar el resultado**
   - Resume la arquitectura elegida y los archivos creados o modificados.
   - Explica servicios, puertos, variables de entorno, almacenamiento persistente y cómo iniciar y detener el entorno.
   - Informa exactamente qué validaciones se ejecutaron y sus resultados, o qué no pudo comprobarse.
   - Señala decisiones pendientes, riesgos de producción y requisitos externos, como una base de datos o secretos que el usuario debe proporcionar.

## Aplicación a este repositorio

- La API Flask está en `api/app.py`, escucha en el puerto `5000` y requiere `DB_HOST`, `DB_USER`, `DB_PASSWORD` y `DB_NAME`.
- El frontend está en `frontend/index.html`, es estático y llama a `/api/tareas`. Una solución Docker debe decidir cómo servirlo y enrutar esas solicitudes a la API; no asumas que abrir el HTML o publicar ambos servicios en puertos distintos funcionará sin configuración adicional.
- La API necesita MySQL disponible, pero este repositorio no tiene configuración Docker, `.env.example` ni pruebas automatizadas. Inspecciona los archivos actuales antes de proponerlos y no inventes credenciales.