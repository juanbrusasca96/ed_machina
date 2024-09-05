```plaintext
- Explicación funcional:

Este proyecto es una solución para el desafío técnico que consiste en desarrollar un sistema de registro de leads de personas que cursan materias en carreras específicas. La solución está compuesta por una API RESTful construida con FastAPI para el backend y una interfaz frontend para gestionar la carga de datos. El backend permite registrar a los leads y consultar los registros cargados de forma paginada.

La API RESTful desarrollada permite:
Registrar personas (leads) que cursan materias que pertenecen a alguna carrera.
Consultar todos los registros de personas de forma paginada.
Consultar un registro específico por su ID.
Verificar si un email ya fue registrado.
Consultar todos los registros de carreras.
Consultar las materias que pertenecen a determinada carrera.

En el frontend la interfaz permite la carga manual de leads con validación de datos antes del envío a la API.

Funcionalidades del Backend:

Registro de Leads: Endpoint para registrar a una persona y la materia y carrera que esta cursando, justo con el año de inscripcion a la carrera, y el tiempo de estudio y cantidad de veces cursada la materia en cuestion. Si el usuario no se encuentra registrado, lo crea y asocia los datos cargados. En el caso de que el usuario ya haya sido registrado asocia los datos cargados a dicho usuario.
Valida los datos de entrada (nombre, email, dirección, teléfono, etc.).
Consulta de Leads Paginados: Endpoint para obtener todos los registros de personas de manera paginada, facilitando la navegación por grandes cantidades de datos.
Consulta de Lead por ID: Endpoint para obtener los detalles de un registro específico mediante su ID.

Funcionalidades del Frontend:

Validacion de email existente: si el email no esta registrado se habilitan los campos de nombre, apellido, direccion y telefono para que el usuario pueda generarse con todos sus datos iniciales. Si el email ya esta registrado estos campos anteriormente mencionados se omiten y solo se permite cargar la carrera, materia, año de inscripcion, tiempo de estudio y cantidad de intentos.
Formulario de Registro: Interfaz de usuario con validación de campos para registrar a una persona y sus materias/carreras.
Confirmación de Registro: Muestra un mensaje de confirmación con el ID del registro creado después de una carga exitosa.

Requisitos del Usuario

El sistema debe permitir a los usuarios:

Registrar una persona con sus datos personales y las materias/carreras que está cursando.
Ver todos los registros paginados de las personas registradas.
Ver detalles de un registro específico mediante su ID.

Flujo de Trabajo

El usuario accede a la API o al frontend para registrar a una persona.
Se ingresan los datos requeridos y se valida la información.
La API procesa la solicitud de registro y almacena la información en una base de datos relacional (PostgreSQL).
El usuario recibe una confirmación del registro con un ID único.
El usuario puede consultar todos los registros de personas o buscar un registro específico utilizando su ID.

- Explicación técnica

Este documento proporciona una guía detallada sobre la arquitectura, la configuración, y la ejecución del proyecto de registro de leads. El backend está construido con FastAPI, y la base de datos utilizada es PostgreSQL. La aplicación está completamente dockerizada para facilitar la configuración y la ejecución en diferentes entornos.

Tecnologías Utilizadas

Python: Lenguaje de programación principal.
FastAPI: Framework para construir la API RESTful.
SQLAlchemy: ORM para manejar las operaciones con la base de datos.
PostgreSQL: Motor de base de datos relacional para almacenamiento persistente.
Docker y Docker Compose: Para contenerizar la aplicación y gestionar los servicios.
React: Biblioteca usada para maquetar el frontend.

Arquitectura del Proyecto

El proyecto está estructurado en capas que separan las responsabilidades principales:

Routes: Define los endpoints de la API.
Services: Contiene la lógica de negocio y las operaciones complejas.
DAOs (Data Access Objects): Maneja las interacciones directas con la base de datos.
Models: Define las entidades y esquemas de la base de datos.
Schemas: Define los modelos de Pydantic para validación y serialización de datos.

Instalación y Configuración

Para ejecutar el proyecto localmente o en un entorno de desarrollo, sigue estos pasos:

1. Clonar el Repositorio dentro de una carpeta

git clone https://github.com/juanbrusasca96/ed_machina.git

2. Construir y Ejecutar el Proyecto con Docker Compose

docker-compose up --build
Dentro de la carpeta backend y frontend

3. Si se desean ejecutar los tests se debe ejecutar el siguiente comando

docker-compose run --rm tests pytest tests/
Dentro de la carpeta backend

Ejecución del Proyecto

Después de configurar el proyecto, puedes acceder a la API en http://localhost:8002/docs
Antes de probar la aplicacion debe correrse el endpoint "/data/upload"

Estructura de Carpetas

.
├── app/
│   ├── __init__.py
│   ├── main.py          # Archivo principal para iniciar la aplicación FastAPI
│   ├── routes/          # Definición de endpoints de la API
│   ├── services/        # Lógica de negocio
│   ├── daos/            # Clases DAO para acceso a datos
│   ├── models/          # Definición de modelos SQLAlchemy
│   ├── schemas/         # Modelos de Pydantic para validación
│   └── utils/           # Funciones utilitarias
├── Dockerfile
├── docker-compose.yml
└── README.md            # Documentación del proyecto

Detalles Técnicos Importantes

Validación de Datos: Se utiliza Pydantic para validar los datos de entrada en la API.
ORM vs SQL Crudo: Se utiliza SQL crudo para ciertas operaciones, gestionadas a través de DAOs, permitiendo un control más directo sobre las consultas SQL.

Endpoints de la API

- **GET /front/person/get_all**: Obtiene todos los registros de personas paginados.
- **GET /front/person/get/{person_id}**: Obtiene un registro de persona por su ID.
- **POST /front/person/register**: Registra un lead en la base de datos.
- **GET /front/person/check_email_exists**: Devuelve un booleano indicando si el email ya se encuentra registrado o no.
- **GET /front/career/get_all**: Obtiene todos los registros de carreras.
- **GET /front/subject/get_by_career/{career_id}**: Obtiene todas las materias que corresponden a una carrera.
