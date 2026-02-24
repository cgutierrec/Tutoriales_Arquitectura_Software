# Proyecto Django: Arquitectura Limpia y APIs Escalables

## Descripcion del Proyecto

Este repositorio documenta la evolucion de un sistema de comercio electronico desarrollado en Django. El proyecto demuestra la transicion de un diseño monolitico acoplado (spaghetti code) hacia una arquitectura profesional de software basada en capas, principios SOLID y patrones creacionales.

---

## Objetivos del Taller

1. Implementar una **Capa de Servicio (Service Layer)** para desacoplar la logica de negocio de los controladores.
2. Aplicar el patron **Factory Method** para gestionar la infraestructura de pagos de forma dinamica.
3. Utilizar el patron **Builder** para la construccion robusta de objetos de dominio complejos.
4. Exponer la logica de negocio a traves de una **API REST** utilizando Django Rest Framework (DRF), permitiendo un enfoque de Backend Headless.

---

## Fases de Desarrollo

### Tutorial 01: Arquitectura SOLID y Capa de Servicio

Se transformo la logica de compra desde vistas funcionales desordenadas hacia una estructura de capas definida para cumplir con el principio de Responsabilidad Unica (SRP).

* **Service Layer**: Creacion de `CompraService` para orquestar la logica de negocio.
* **Inversion de Dependencias**: El sistema depende de abstracciones para el procesamiento de pagos.
* **Evidencia**: Registro de auditoria en el archivo `pagos_locales_CRISTOBAL_FLOREZ.log`.

### Tutorial 02: Patrones Creacionales (Factory & Builder)

* **Factory Method**: Implementacion de `PaymentFactory` que lee la variable de entorno `PAYMENT_PROVIDER`. Permite alternar entre un procesador de pagos real y un `MockPaymentProcessor` para pruebas de desarrollo.
* **OrdenBuilder**: Diseño de un constructor fluido para el modelo `Orden`, encapsulando el calculo de impuestos (IVA 19%) y garantizando la integridad de los datos antes de la persistencia.

### Tutorial 03: Backend Headless (API REST con DRF)

Se integro Django Rest Framework para permitir que clientes externos realicen compras mediante peticiones JSON, demostrando que la arquitectura es independiente del cliente (Web o App).

* **Reutilizacion**: La API utiliza el mismo `CompraService` que la interfaz HTML.
* **Endpoint**: `POST /api/v1/comprar/`
* **Serializacion**: Uso de `Serializers` como adaptadores para la validacion y transformacion de datos JSON a objetos de Python.

---

## Estructura de la Solucion (Clean Architecture)

* **tienda_app/domain/**: Logica pura de negocio y constructores (Builders).
* **tienda_app/infra/**: Adaptadores de infraestructura y fabricas (Gateways, Factories).
* **tienda_app/api/**: Capa de entrada para clientes REST (Serializers, APIViews).
* **tienda_app/services.py**: Orquestador que vincula todas las capas.

---

## Instrucciones de Configuracion y Ejecucion

### Modos de Ejecucion

El sistema se adapta al entorno segun la configuracion de la terminal:

* **Modo Produccion (Log Real)**:

  ```cmd
  python manage.py runserver
  ```

* **Modo Desarrollo (Debug Mock)**:

  ```cmd
  set PAYMENT_PROVIDER=MOCK && python manage.py runserver
  ```

### Pruebas de API

Para realizar una compra via API, enviar una peticion POST a `/api/v1/comprar/` con el siguiente cuerpo:

```json
{
    "libro_id": 2,
    "direccion_envio": "Direccion de prueba API"
}
```

---

## Tecnologias Utilizadas

* Python 3.11
* Django 5.2.11
* Django Rest Framework (DRF)
* Git: Flujo de trabajo basado en ramas (`feature/solid`, `feature/tutorial-02`, `feature/tutorial-03`).