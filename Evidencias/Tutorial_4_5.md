
# Tutorial 04 y 05: Docker, Nginx y Gunicorn

## Tutorial 04 — Dockerización

Nombre: Cristobal Gutierrez

Antes de este tutorial la app solo corría localmente con SQLite y `runserver`. El objetivo era empaquetarla en Docker y desplegarla en AWS EC2.

Lo primero fue ajustar `settings.py` para leer las credenciales de la base de datos desde variables de entorno en lugar de tenerlas escritas a mano. Luego se creó el `Dockerfile` con Python 3.11-slim y se generó `requirements.txt` con todas las dependencias, incluyendo `psycopg2-binary` y `gunicorn` que no estaban antes.

El `docker-compose.yml` levanta dos servicios: PostgreSQL en un contenedor y Django en otro, conectados por red interna. Localmente funcionó sin problemas. En EC2 hubo un inconveniente: la versión de Docker en Amazon Linux 2023 no incluye el plugin `compose` ni `buildx` por defecto. Hubo que instalar ambos manualmente descargando los binarios desde GitHub. El buildx versión `latest` también falló porque el redirect de GitHub devolvía 9 bytes en lugar del binario real — se resolvió especificando la versión `v0.17.0` directamente en la URL.

**Evidencia:** API respondiendo en `http://<IP-EC2>:8000/api/v1/comprar/` desde AWS.

---

## Tutorial 05 — Nginx + Gunicorn

`runserver` no es para producción. Gunicorn maneja las peticiones Python de forma correcta, y Nginx actúa como proxy inverso adelante de todo.

Los cambios fueron tres: crear `nginx/nginx.conf` con la configuración del upstream hacia el servicio `web`, actualizar `docker-compose.yml` para agregar el servicio `nginx` en el puerto 80 y cambiar el comando de arranque de Django a `gunicorn Tienda.wsgi:application`, y quitar la exposición directa del puerto 8000 al exterior.

Con esto Django queda completamente aislado — solo Nginx puede hablarle por la red interna de Docker. Intentar acceder a `:8000` desde fuera da timeout, que es exactamente lo que se busca.

En EC2 el despliegue fue directo: `git fetch`, checkout de la rama, `docker compose down` y `docker compose up -d --build`. Los tres contenedores (db, web, nginx) levantaron sin errores.

**Evidencias:**
- Navegador accediendo a `http://<IP-EC2>/api/v1/comprar/` sin puerto — Nginx enrutando por el 80.
- Timeout al intentar `http://<IP-EC2>:8000` — Django aislado correctamente.
- `docker ps` mostrando los tres contenedores en estado `Up`.

---

## Estructura del proyecto

```
.
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── nginx/
│   └── nginx.conf
├── Tienda/
│   └── settings.py
└── tienda_app/
```

## Comandos clave

```bash
# Levantar todo
docker compose up -d --build

# Aplicar migraciones
docker exec <contenedor-web> python manage.py migrate

# Ver contenedores activos
docker ps

# Bajar todo
docker compose down
```