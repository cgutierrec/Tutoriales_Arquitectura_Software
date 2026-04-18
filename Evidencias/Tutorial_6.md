# Tutorial 06: El Primer Estrangulamiento — Strangler Pattern con Flask

## Qué se hizo

El objetivo era extraer la función de compras del monolito Django y moverla a un microservicio Flask independiente, sin que el usuario final note el cambio. Nginx actúa como el cerebro del ruteo: decide a quién enviar cada petición según la versión de la API.

La arquitectura quedó así:

- `/api/v1/comprar/` → sigue yendo a Django (el monolito original)
- `/api/v2/comprar` → va al microservicio Flask (el estrangulador)

Ambos conviven en el mismo `docker-compose.yml` y Nginx los coordina sin que ninguno sepa del otro.

---

## Archivos nuevos

`microservicio_pagos/app.py` — el microservicio Flask con un endpoint POST que simula la lógica de compra y responde con un JSON confirmando que procesó la orden el servicio v2.

`microservicio_pagos/Dockerfile` — imagen Alpine con Python 3.11, Flask y Gunicorn. Ligera a propósito.

---

## Cambios en archivos existentes

`nginx/nginx.conf` — se agregaron dos upstreams: `django_v1` apuntando al servicio `web:8000` y `flask_v2` apuntando a `pagos_flask:5000`. Nginx rutea por prefijo de URL.

`docker-compose.yml` — se añadió el servicio `pagos_flask` construido desde `./microservicio_pagos`. El servicio `nginx` ahora depende tanto de `web` como de `pagos_flask`.

---

## Evidencias

- POST a `http://<IP-EC2>/api/v1/comprar/` → responde Django con 201 y el total de la orden.
- POST a `http://<IP-EC2>/api/v2/comprar` → responde Flask con 200 y el mensaje "Compra procesada exitosamente por el Microservicio Flask (v2)".
- `docker compose logs nginx` → muestra las peticiones redirigidas a los dos backends distintos.

---

## Por qué funciona

El Strangler Pattern no requiere reescribir todo de golpe. Se introduce el nuevo servicio en paralelo y se redirige tráfico gradualmente. En este caso Nginx es el punto de control: con un bloque `location` adicional en su configuración basta para que una ruta entera cambie de backend sin tocar una línea de Django.