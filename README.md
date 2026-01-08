# 📘 FastAPI CRUD – MongoDB & PostgreSQL

Este proyecto implementa una **API REST CRUD** utilizando **FastAPI**, con una arquitectura híbrida que integra **MongoDB** y **PostgreSQL**, permitiendo manejar distintos tipos de datos según su naturaleza y necesidad.

La aplicación está diseñada de forma modular, facilitando la escalabilidad, el mantenimiento y la extensión a nuevos módulos o bases de datos.

---

## 🧩 Tecnologías Utilizadas

* **Python 3.10+**
* **FastAPI** – Framework web moderno y de alto rendimiento
* **MongoDB** – Base de datos NoSQL orientada a documentos
* **PostgreSQL** – Base de datos relacional
* **Motor / PyMongo** – Cliente asíncrono para MongoDB
* **SQLAlchemy** – ORM para PostgreSQL
* **Pydantic** – Validación y serialización de datos
* **Docker & Docker Compose** – Orquestación de servicios (opcional)
* **Uvicorn** – Servidor ASGI

---

## 🧠 Arquitectura General

El proyecto implementa una **arquitectura híbrida de persistencia**:

* **MongoDB**

  * Datos flexibles
  * Documentos sin esquema rígido
  * Operaciones CRUD rápidas
* **PostgreSQL**

  * Datos estructurados
  * Relaciones y consistencia
  * Casos donde se requiere integridad referencial

Cada base de datos cuenta con su propia capa de conexión y acceso.

---

## 📁 Estructura del Proyecto

```
fastapi_crud_mng_pg/
├── app/
│   ├── main.py                     # Inicialización de FastAPI
│   ├── routers/                    # Endpoints de la API
│   │   ├── mongo/                  # Rutas que usan MongoDB
│   │   └── postgres/               # Rutas que usan PostgreSQL
│   ├── schemas/                    # Esquemas Pydantic
│   ├── crud/                       # Lógica de negocio CRUD
│   ├── database/
│   │   ├── mongo/                  # Conexión y cliente MongoDB
│   │   │   ├── connection.py
│   │   │   └── config.py
│   │   └── postgres/               # Conexión PostgreSQL (SQLAlchemy)
│   │       ├── session.py
│   │       └── base.py
│   ├── models/                     # Modelos SQLAlchemy (PostgreSQL)
│   └── core/                       # Configuración y utilidades
├── docker-compose.yml              # Servicios Docker
├── requirements.txt                # Dependencias del proyecto
└── README.md
```


<img width="1094" height="630" alt="image" src="https://github.com/user-attachments/assets/ade11a3e-629f-4fc5-b865-7b8b1c1f1f6f" />

---

## 🔌 Conexión a Bases de Datos

### 🍃 MongoDB

La conexión a MongoDB se gestiona desde:

```
app/database/mongo
```

Usando un cliente asíncrono (`motor` o `pymongo`) para acceder a las colecciones.

Ejemplo conceptual:

```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]
```

---

### 🐘 PostgreSQL

La conexión a PostgreSQL se maneja mediante **SQLAlchemy**, con sesiones controladas desde:

```
app/database/postgres
```

Incluye:

* Engine
* SessionLocal
* Modelos relacionales

---

## ⚙️ Variables de Entorno

Crea un archivo `.env` con la siguiente configuración:

```env
# MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=app_db

# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=app_db
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app_db
```

---

## 🚀 Ejecución del Proyecto

### ▶️ Local

```bash
python entrypoint.py
```

La API estará disponible en:

```
http://localhost:8000
```

Documentación automática:

* Swagger: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

---

### 🐳 Con Docker

```bash
docker compose up -d
```

Esto levantará:

* FastAPI
* MongoDB
* PostgreSQL

---

## 📍 Ejemplo de Endpoints

### MongoDB

```
GET    /mongo/items
POST   /mongo/items
PUT    /mongo/items/{id}
DELETE /mongo/items/{id}
```

### PostgreSQL

```
GET    /postgres/users
POST   /postgres/users
PUT    /postgres/users/{id}
DELETE /postgres/users/{id}
```

*(Las rutas pueden variar según el módulo implementado)*

---

## 📈 Buenas Prácticas Implementadas

* Separación clara por capas
* Conexiones desacopladas por base de datos
* Validaciones con Pydantic
* Arquitectura extensible
* Preparado para autenticación y testing
