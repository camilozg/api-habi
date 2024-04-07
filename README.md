
# Prueba Habi

## Servicio de consulta

Para el desarrollo del API que permita a los usuarios consultar inmuebles utilizaré principalmente las siguientes tecnologías y/o librerías:

* http.server
* configparser
* pytest
* requests

El desarrollo será abordado con el enfoque TDD (Test-Driven Development) mediante el cual se construirán las pruebas unitarias antes de desarrollar el API para luego validar y realizar la refactorización del código.

De esta manera, desarrollaré un API que cuente con un endpoint que permita realizar peticiones tipo GET con los parámetros de búsqueda especificados en los requerimientos.

**Ejemplos de llamadas al API:**

* http://localhost:8000/api/property?city=bogota

* http://localhost:8000/api/property?year=2021

* http://localhost:8000/api/property?status=pre_venta

* http://localhost:8000/api/property?city=pereira&status=pre_venta&year=2021

**Nota:** En el desarrollo del API no he creado el archivo JSON que simula la llegada desde el front end ya que envió los parámetros de los filtros a través de la URL.

## Servicio de “Me gusta”

Este servicio implica una relación de muchos a muchos entre usuarios y propiedades, por lo que es necesario la creación de una tercera tabla que permita identificar los "me gusta" asociados a estas entidades. De esta manera, para dar solución a este requerimiento, se propone la creación de la tabla "user" y la tabla "like_history", en adición a las ya existentes.

* **Diagrama entidad relación:**

![alt text](/segundo-servicio/ERD.jpg)

* **Código SQL para las nuevas tablas:**

``` sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE like_history (
    id INT PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (property_id) REFERENCES property(id)
);
```