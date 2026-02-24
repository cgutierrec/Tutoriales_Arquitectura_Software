# Proyecto Django SOLID: Taller de Arquitectura de Software

## Descripcion del Proyecto
Este proyecto consiste en la implementacion de una tienda de libros utilizando el framework Django, con un enfoque progresivo desde una arquitectura monolitica acoplada hacia una arquitectura limpia basada en los principios SOLID y patrones de diseño empresariales.

---

## Objetivos del Taller
1. Demostrar la transicion de codigo spaghetti hacia una estructura desacoplada.
2. Implementar la inyeccion de dependencias para el procesamiento de pagos.
3. Utilizar el patron de diseño Builder para la creacion de ordenes complejas.
4. Aplicar el patron Factory para la gestion de proveedores de infraestructura.
5. Garantizar la trazabilidad de las operaciones mediante logs personalizados.

---

## Fases de Implementacion

### Paso 1: Vista Basada en Funciones (FBV) Spaghetti
Se desarrollo una primera version de la compra de libros directamente en el archivo views.py. En esta etapa, la vista era responsable de validar el inventario, calcular impuestos de forma manual, escribir directamente en el sistema de archivos para registrar el pago y crear el registro en la base de datos. Esta fase evidencio violaciones a los principios de Responsabilidad Unica (SRP) e Inversion de Dependencias (DIP).

### Paso 2: Vista Basada en Clases (CBV)
Se realizo la refactorizacion de la interfaz hacia Clases Basadas en Vistas. Esto permitio separar los metodos GET y POST, preparando el terreno para la inyeccion del servicio de negocio.

### Paso 3: Capa de Servicio e Infraestructura (SOLID)
Se implemento la arquitectura final dividida en las siguientes capas:
* **Capa de Dominio**: Contiene la logica pura de negocio, como el CalculadorImpuestos y el OrdenBuilder para la construccion de objetos Orden.
* **Capa de Servicio**: El archivo services.py actua como orquestador, recibiendo dependencias externas y coordinando las acciones entre el dominio y la base de datos.
* **Capa de Infraestructura**: Implementacion de Gateways y Factories para el procesamiento de pagos sin acoplar la logica de negocio a proveedores especificos.

---

## Patrones de Diseño Utilizados
* **Builder**: Utilizado para construir la instancia de Orden de manera fluida, asegurando que todos los campos requeridos se validen antes de la persistencia.
* **Factory**: Utilizado para instanciar el procesador de pagos (BancoNacionalProcesador) de manera que la vista no conozca la implementacion concreta.
* **Dependency Injection**: El servicio de compra recibe a traves de su constructor el motor de pagos, facilitando las pruebas unitarias y el intercambio de proveedores.

---

## Evidencias de Ejecucion
Se realizaron pruebas de funcionalidad ejecutando compras multiples. La correcta operacion del sistema se verifica mediante:
1. Actualizacion automatica del stock en la tabla Inventario.
2. Persistencia de registros en la tabla Orden.
3. Generacion de un archivo de log especializado llamado pagos_locales_CRISTOBAL_FLOREZ.log, el cual documenta cada transaccion procesada por la capa de infraestructura.

---

## Tecnologias Empleadas
* Python 3.11
* Django 5.2.11
* SQLite3
* Git para el control de versiones por ramas (feature/fbv-spaghetti y feature/solid-architecture).