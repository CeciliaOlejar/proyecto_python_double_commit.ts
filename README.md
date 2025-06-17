|  ConstruRent |
| ------------ |

# 🛠️ Catálogo de Herramientas para Alquiler

Aplicación desarrollada en Python para gestionar un catálogo de herramientas disponibles para **alquiler**, con control de **usuarios**, **registro de herramientas**, y **seguimiento de tiempo de alquiler**.

## 🚀 Funcionalidades principales

- Registro e inicio de sesión de usuarios
- Catálogo de herramientas disponibles para alquilar
- Alquiler de herramientas con control de tiempo
- Asistente IA integrado al sistema
- Devolución de herramientas
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
python -m venv .venv # Windows

python3 -m venv .venv # Linux / MacOs
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
├── main.py
├── controller/
│   ├── asistente.py
│   └── usuario.py
├── db/
│   └── conexion.py
├── models/
│   ├── usuario.py
│   └── herramienta.py
├── alquiler/
│   └── gestion_alquiler.py
├── styles/
│   └── Menu.py
├── utils/
│   ├── efecto.py
│   └── resaltar.py
├── venv/*
├── .env
├── requirements.txt
├── README.md
└── README.md
```

---

<div align="center">
   ConstruRent • doubleCommit.ts 2025
</div>
