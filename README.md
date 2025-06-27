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

### 📦 Estructura del proyecto

```bash
proyecto/
├── alquiler/
│   └── gestion_alquiler.py
├── controller/
│   ├── asistente.py  
│   ├── herramienta.py
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
│   ├── cohere_config.py
│   ├── efecto.py
│   ├── resaltar.py
│   └── ubicacion.py
├── venv/*
├── .env
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
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    descripcion TEXT,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    fecha_adquisicion DATE NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    precio_por_dia DECIMAL(10,2) NOT NULL CHECK (precio_por_dia > 0),
    estado VARCHAR(20) DEFAULT 'Disponible' CHECK (estado IN ('Disponible', 'Alquilado', 'En Mantenimiento', 'Fuera de Servicio'))
);
```
- Crear tabla para usuarios:
```sql
-- Crear tabla usuario
CREATE TABLE usuario (
   id_usuario SERIAL PRIMARY KEY,
   nombre VARCHAR(30) NOT NULL,
   apellido VARCHAR(30) NOT NULL,
   email VARCHAR(50) NOT NULL,
   contrasenia VARCHAR(50) NOT NULL
)
```

### Para la conexión a la BD

- Hemos usado la librería `python-dotenv` para poder crear variables de entorno de manera segura en nuestro archivo.

Crearemos un archivo `.env` con las siguientes variables de entorno:
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
