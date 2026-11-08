# Gestión del Estrés Universitario – Módulo Administrador

Aplicación web en **Flask (MVC)** que gestiona los datos que alimentan al core de una app de manejo del estrés académico para estudiantes universitarios.

**Demo:** https://proyecto-estres-estudiantil.onrender.com
**Video:**https://youtu.be/3tHNhoPd2OM

---

## ¿Qué hace?

El **core** calcula el estado de cada estudiante con dos fórmulas:

- **Carga académica** = Σ peso(evento)
- **Estrés promedio** = Σ nivel / n

Con estos valores clasifica al estudiante en **Normal**, **Atención** o **Crítico** y le recomienda técnicas de manejo del estrés según su **arquetipo** (Introspectivo, Kinestésico, Creador, Analítico, Social).

El **módulo administrador** alimenta y supervisa ese proceso:

| Sección | Función |
|---|---|
| **Usuarios** | Crear usuarios (Estudiante / Administrador) con su arquetipo |
| **Eventos académicos** | Supervisar los eventos que registran los estudiantes |
| **Técnicas** | Gestionar el catálogo de técnicas por arquetipo (crear y eliminar las agregadas por el admin) |
| **Alertas** | Registrar alertas de seguimiento manual con una técnica recomendada |

El estudiante ve en su **dashboard** las alertas que le asignaron.

---

## Requisitos del admin

### 1. Validación en el back-end de un dato sensible del core
En **Alertas**, la técnica recomendada y el estudiante **deben pertenecer al mismo arquetipo**. Si se asignara una técnica de otro arquetipo, se rompería la lógica de recomendaciones del core. El servidor lo verifica aunque se manipule el HTML y responde **HTTP 400**.

Otras validaciones del back-end:
- **Correo**: obligatorio, formato válido, máximo 100 caracteres, único y normalizado a minúsculas.
- **Contraseña**: mínimo 8 caracteres, con mayúscula, minúscula y número. Se guarda con hash **scrypt**.
- **Rol**: solo `Estudiante` o `Administrador`. El registro público siempre crea **Estudiante**.
- **Técnicas**: no se repiten dentro del mismo arquetipo. Las predeterminadas y las que ya están en uso en una alerta no se pueden eliminar.
- **Llaves foráneas**: el servidor comprueba que el id recibido exista en la BD.

### 2. Llaves foráneas con dropdown y cascada
Ninguna FK se escribe a mano: todas se eligen con un `<select>` cargado desde la base de datos.

**Dropdown en cascada** (formulario de alertas):
```
Arquetipo  ──►  Estudiantes de ese arquetipo
           └─►  Técnicas de ese arquetipo
```
Al escoger el arquetipo, el servidor recarga el formulario solo con sus estudiantes y técnicas (cascada resuelta del lado del servidor, sin JavaScript).

---

## Tecnologías

- Python 3.13 · Flask · Jinja2
- MySQL 8 (Aiven) · mysql-connector-python
- Werkzeug (hash de contraseñas)
- Sass con nomenclatura **BEM**
- Gunicorn (despliegue en Render)

---

## Estructura del proyecto

```
├── app.py                  # Punto de entrada, registra los blueprints
├── config.py               # Lee las variables del .env
├── database.py             # Conexión a MySQL (SSL con ca.pem en la nube)
├── controllers/            # Controladores (Blueprints)
│   ├── admin_controller.py #   /admin/*   (solo Administrador)
│   ├── auth_controller.py  #   /login, /logout, /registro
│   └── core_controller.py  #   /core/*    (solo Estudiante)
├── models/                 # Consultas SQL parametrizadas
├── views/                  # Plantillas Jinja (admin, auth, core)
├── utils/
│   ├── validaciones.py     # Validaciones del back-end
│   └── auth.py             # Protección de rutas por rol
├── static/scss/            # Estilos Sass (BEM) y CSS compilado
└── sql/creacion_DB.sql     # Esquema de la BD + datos iniciales
```

---

## Instalación local

### 1. Clonar e instalar
```bash
git clone https://github.com/Lapuchulfa/Proyecto-Estres-Estudiantil.git
cd Proyecto-Estres-Estudiantil
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / Mac
pip install -r requirements.txt
```

### 2. Crear la base de datos
Ejecuta `sql/creacion_DB.sql` en MySQL. Crea las tablas, los 5 arquetipos con 4 técnicas cada uno y el administrador inicial.

### 3. Variables de entorno
Crea un archivo **`.env`** en la raíz (no se sube a Git):
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=estres_universitario
SECRET_KEY=una_clave_larga_y_aleatoria
```
Para generar una `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Si `DB_HOST` no es `localhost`, la conexión usa SSL con el certificado `ca.pem`.

### 4. Ejecutar
```bash
python app.py
```
Abre http://127.0.0.1:5000

---

## Administrador inicial

Los administradores **no se registran públicamente**: el primero se inserta en la BD y los siguientes los crea un admin desde el panel.

Para crear uno con tu propia contraseña:
```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('TuPassword1'))"
```
```sql
INSERT INTO usuario (nombre_usuario, apellido_usuario, correo_usuario, password_hash, rol)
VALUES ('Admin', 'Sistema', 'admin@udla.edu.ec', '<hash generado>', 'Administrador');
```

---

## Rutas principales

| Ruta | Acceso | Descripción |
|---|---|---|
| `/login`, `/registro` | Público | Inicio de sesión y registro de estudiantes |
| `/admin/usuarios` | Admin | Lista y creación de usuarios |
| `/admin/eventos` | Admin | Supervisión de eventos académicos |
| `/admin/tecnicas` | Admin | Catálogo de técnicas |
| `/admin/alertas` | Admin | Alertas de seguimiento (cascada) |
| `/core/dashboard` | Estudiante | Alertas del estudiante |

---

## Seguridad

- Contraseñas con hash **scrypt**, nunca en texto plano.
- **Consultas parametrizadas** (`%s`) contra la inyección SQL.
- Protección por rol con `before_request` en cada blueprint.
- Mismo mensaje de error en el login, para no revelar qué correos existen.
- Acciones que modifican datos (logout, eliminar) solo por **POST**.
- Credenciales en `.env`, excluido del repositorio.

---

## Despliegue (Render)

1. Nuevo **Web Service** conectado al repositorio.
2. **Build command:** `pip install -r requirements.txt`
3. **Start command:** `gunicorn app:app`
4. En **Environment**, agregar las mismas variables del `.env`.

---

## Próximos pasos (core)

- Cuestionario al primer ingreso para determinar el arquetipo del estudiante.
- Check-in de nivel de estrés (1–10) e historial.
- Registro de eventos por el estudiante, con validación del peso según el tipo (función `validar_evento` ya implementada).
- Cálculo de carga y estrés promedio, y alertas automáticas al llegar a *Crítico*.
- Mejoras futuras: notificación por correo, integración con calendarios externos y actividades de bienestar.
