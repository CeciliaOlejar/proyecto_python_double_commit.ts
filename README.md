# 🛠️ Catálogo de Herramientas para Alquiler

Aplicación desarrollada en Python para gestionar un catálogo de herramientas disponibles para **alquiler**, con control de **usuarios**, **registro de herramientas**, y **seguimiento de tiempo de alquiler**.

## 🚀 Funcionalidades principales

- Registro e inicio de sesión de usuarios
- Catálogo de herramientas disponibles para alquilar
- Alquiler de herramientas con control de tiempo
- Devolución de herramientas
- Historial de alquileres por usuario

## 🧰 Tecnologías utilizadas

- Python 3.11
- PostgreSQL (base de datos)
- `psycopg2` o `psycopg2-binary` (conexión a la base de datos)
- Interfaz por consola (CLI)

## 🔧 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tu_usuario/nombre-del-repo.git
cd nombre-del-repo
```

2. Crear y activar el entorno virtual

```bash
python -m venv venv
source venv/Scripts/activate  # En Windows
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 📦 Estructura del proyecto

```bash
proyecto/
├── venv/
├── main.py
├── db/
│   └── conexion.py
├── models/
│   ├── usuario.py
│   └── herramienta.py
├── alquiler/
│   └── gestion_alquiler.py
├── requirements.txt
└── README.md
```

