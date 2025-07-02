|  ConstruRent |
| ------------ |

# 🛠️ Catálogo de Herramientas para Alquiler

Aplicación desarrollada en Python puro para gestionar un catálogo de herramientas disponibles para **alquiler**, con control de **usuarios**, **registro de herramientas**, **asistente IA** y **seguimiento de tiempo de alquiler**.

## 🚀 Funcionalidades principales

- Registro e inicio de sesión de usuarios
- Catálogo de herramientas disponibles para alquilar
- Alquiler de herramientas con control de tiempo
- Asistente IA integrado al sistema
- El asistente IA puede hacer web scrapping si no tiene información reciente
- Historial de alquileres por usuario

## 🧰 Tecnologías utilizadas

- Python 3.11
- PostgreSQL (base de datos)
- `psycopg2` (conexión a la base de datos)
- `cohere` IA (Asistente inteligencia artificial)
- Interfaz por consola (CLI)


## 📼 Link al Video sobre la app

https://drive.google.com/drive/u/1/folders/1VMJW0DNvWXzwmynGQ_Ji_HurUZvVqRkN

## 🔧 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/PowerSystem2024/proyecto_python_double_commit.ts.git
cd proyecto_python_double_commit
```

2. Crear el entorno virtual
```bash
python -m venv venv # Windows

python3 -m venv venv # Linux / MacOs
```
- Activar el entorno virtual
```bash
python -m venv venv
source venv/Scripts/activate  # En Windows

source .venv/bin/activate # Linux / MacOS
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

4. Para utilizar el asistente IA con web scraping, es necesario instalar los binarios de los motores (Chromium):

```bash
playwright install
```

5. Para poder utilizar el modelo IA es necesario que obtengas tu <<api_key>> gratuita de cohere, en el siguiente link se explica
que puedes hacer con su modelo, lo recomiendo para que puedan practicar y hacer diferentes tipos de aplicaciones con IA: [Documentación Cohere](https://docs.cohere.com/reference/about)

### 📦 Estructura del proyecto

```bash
proyecto/
├── alquiler/
│   └── gestion_alquiler.py
├── controller/
│   ├── asistente.py  
│   ├── herramienta.py
│   ├── manejador_opciones.py
│   ├── ticket.py
│   └── usuario.py
├── db/
│   └── conexion.py
├── models/
│   ├── Herramienta.py
│   ├── Ticket-py 
│   └── Usuario.py
├── styles/
│   └── Menu.py
├── utils/
│   ├── buscador.py
│   ├── cohere_config.py
│   ├── resaltar.py    
│   ├── efecto.py
│   ├── resaltar.py
│   └── ubicacion.py
├── venv/*
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

### Instrucciones para crear la BD

- Crear base de datos:
```sql
-- Crear base de datos construrent
CREATE DATABASE construrent
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_ES.UTF-8'
    LC_CTYPE = 'es_ES.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
```
- Crear tabla para herramientas:
```sql
-- Crear tabla herramienta
CREATE TABLE herramienta (
    id_herramienta SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipo VARCHAR(100),
    descripcion TEXT,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    fecha_adquisicion DATE,
    ubicacion VARCHAR(150),
    estado VARCHAR(20) DEFAULT 'Disponible' CHECK (estado IN ('Disponible', 'Alquilado', 'En Mantenimiento', 'Fuera de Servicio'))
    precio_por_dia NUMERIC(10, 2)
);
```
- Crear tabla para usuarios:
```sql
-- Crear tabla usuario
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    contrasenia VARCHAR(255) NOT NULL,
    rol NUMERIC(2,0) NOT NULL
);
```
- Crear tabla para tickets:
```sql
-- Crear tabla ticket
CREATE TABLE ticket (
    idticket SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuario(id_usuario),
    id_herramienta INTEGER REFERENCES herramienta(id_herramienta),
    estado_ticket VARCHAR(50),
    cliente VARCHAR(150),
    nombre VARCHAR(150),
    tipo VARCHAR(100),
    modelo VARCHAR(100),
    marca VARCHAR(100),
    descripcion VARCHAR(255),
    fecha_adquisicion DATE,
    precio_por_dia NUMERIC(10, 2),
    ubicacion VARCHAR(150),
    fecha_inicio DATE,
    fecha_fin DATE
);
```
- Insertar herramientas basicas iniciales:
```sql
-- Opcional, solo se pueden registrar desde un Usuario Admin

INSERT INTO herramienta (
    nombre,
    tipo,
    descripcion,
    marca,
    modelo,
    fecha_adquisicion,
    ubicacion,
    precio_por_dia,
    estado
) VALUES
('Taladro Percutor', 'Eléctrica', 'Taladro percutor de 750W para mampostería y metal', 'Bosch', 'GSB-16RE', '2022-05-10', 'Depósito A', 1500.00, 'Disponible'),
('Amoladora Angular', 'Eléctrica', 'Amoladora de 115mm, 900W', 'Makita', 'GA4530', '2023-01-20', 'Depósito B', 1200.00, 'Disponible'),
('Cortadora de Cerámica', 'Manual', 'Cortadora de cerámica de 60cm', 'Rubi', 'Star-60', '2021-08-15', 'Depósito A', 800.00, 'Disponible'),
('Martillo Demoledor', 'Eléctrica', 'Martillo demoledor SDS-Max', 'DeWalt', 'D25899K', '2022-11-05', 'Depósito C', 2500.00, 'Disponible'),
('Sierra Circular', 'Eléctrica', 'Sierra circular 1600W para madera', 'Black & Decker', 'CS1000', '2023-04-12', 'Depósito B', 1800.00, 'Disponible');



### Para la conexión a la BD

- Hemos usado la librería `python-dotenv` para poder crear variables de entorno de manera segura en nuestro archivo.

Crearemos un archivo `.env` con las siguientes variables de entorno:
- Esto nos sirve para que no se suban nuestras claves importantes y no nos `hard-codeen` nuestras APIS_KEY 😨..
- Siempre y cuando hayamos ignorado en nuestro hermoso `.gitignore` los `.env` o `.env.*`
```bash
COHERE_API_KEY="<<TU_API_KEY_DE_COHERE>>"
DB_USER="<<TU_USUARIO_DE_BASE_DE_DATOS>>"
DB_PASSWORD="<<TU_CONTRASEÑA_DE_BASE_DE_DATOS>>"
```

Que más adelante las llamaremos desde la clase Conexión
```python
import psycopg2 as bd
import sys, os
from dotenv import load_dotenv

load_dotenv() # Esta función carga el archivo .env y localiza las variables de entorno dentro de él
USERNAME_DB = os.getenv("DB_USER") # LLamamos al nombre de la variable de entorno
PASSWORD_DB = os.getenv("DB_PASSWORD")

class Conexion:
    _DATABASE = "construrent"
    _USERNAME = USERNAME_DB
    _PASSWORD = PASSWORD_DB
    _PORT = "5432"
    _HOST = "127.0.0.1"
    _conexion = None
    _cursor = None

    @classmethod
    def obtener_conexion(cls):
        if cls._conexion is None:
            try:
                cls._conexion = bd.connect(
                    host=cls._HOST,
                    user=cls._USERNAME,
                    password=cls._PASSWORD,
                    port=cls._PORT,
                    database=cls._DATABASE,
                )
                return cls._conexion
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                sys.exit()
        else:
            return cls._conexion
```
---

<div align="center">
   ConstruRent • doubleCommit.ts 2025
</div>
