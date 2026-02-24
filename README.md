# Proyecto Django: Arquitectura de Software y Patrones Creacionales

## Descripcion del Proyecto
Este repositorio documenta la evolucion de un sistema de comercio electronico desarrollado en Django, transitando desde un diseño monolitico funcional hasta una arquitectura desacoplada basada en principios SOLID y patrones creacionales de diseño (Factory Method y Builder).

---

## Objetivos del Taller
1. Aplicar los principios SOLID para reducir el acoplamiento y aumentar la cohesion del codigo.
2. Implementar el patron Factory Method para la gestion dinamica de infraestructura mediante variables de entorno.
3. Utilizar el patron Builder para la construccion de objetos de dominio complejos, asegurando la integridad de los datos.
4. Establecer un flujo de trabajo profesional mediante el uso de ramas en Git.

---

## Fases de Desarrollo

### Tutorial 01: Arquitectura SOLID y Service Layer
En esta fase se transformo una vista funcional desordenada (spaghetti) en una estructura de capas:
* **Service Layer**: Se creo la clase CompraService para orquestar la logica de negocio, separandola de la logica de presentacion.
* **Inversion de Dependencias**: Se definieron interfaces para el procesamiento de pagos, permitiendo que el sistema dependa de abstracciones y no de implementaciones concretas.
* **Evidencia**: Generacion de logs de auditoria personalizados (pagos_locales_CRISTOBAL_FLOREZ.log).

### Tutorial 02: Patrones Creacionales
Se optimizo la creacion de objetos mediante patrones especificos:
* **Factory Method**: Implementado en la clase PaymentFactory. Este componente permite inyectar diferentes procesadores de pago (Banco Real o Mock de Pruebas) basandose en la variable de entorno PAYMENT_PROVIDER. Esto permite que la aplicacion sea Docker-Ready y facilite las pruebas unitarias.
* **Patron Builder**: Implementado en la clase OrdenBuilder. Se utiliza para ensamblar objetos de tipo Orden de forma fluida, encapsulando el calculo de impuestos (IVA 19%) y validando que los productos y el usuario esten presentes antes de la persistencia.

---

## Estructura de la Solucion
* **tienda_app/domain**: Contiene la logica pura de negocio y los constructores (Builders).
* **tienda_app/infra**: Aloja los Gateways para comunicacion con servicios externos y las Fabricas (Factories).
* **tienda_app/services.py**: Actua como mediador entre las vistas y el dominio.
* **tienda_app/views.py**: Vistas basadas en clases (CBV) que actuan como puntos de entrada agnosticos a la implementacion.

---

## Instrucciones de Ejecucion y Pruebas

### Modo Produccion (Banco Real)
Para ejecutar el sistema utilizando la infraestructura de pagos real:
python manage.py runserver

### Modo Desarrollo (Mock Payment)
Para ejecutar el sistema en modo de pruebas y observar los mensajes de depuracion por consola (CMD):
set PAYMENT_PROVIDER=MOCK && python manage.py runserver

---

## Tecnologias Empleadas
* Python 3.11
* Django 5.2.11
* SQLite3
* Control de versiones: Git (Flujo basado en ramas por caracteristicas).