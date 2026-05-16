# TechStore — E-commerce Django Módulos 6, 7 y 8

Aplicación e-commerce desarrollada con Django. Integra autenticación, catálogo persistente con ORM, CRUD administrativo de productos, carrito de compras y registro de pedidos.

**Demo live:** https://darwinhans.pythonanywhere.com

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin_demo` | `Admin12345` |
| Cliente | `cliente_demo` | `Cliente12345` |

**Stack:** Django 6.0.3 · SQLite · Python 3.12 · desplegado en PythonAnywhere (free tier).

---

## Requisitos previos

- Python 3.10 o superior
- pip

---

## Pasos para ejecutar el proyecto

**1. Clonar o descomprimir el proyecto**

**2. Crear y activar el entorno virtual**

```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Instalar dependencias**

```bash
pip install django
```

**4. Aplicar migraciones**

```bash
python manage.py migrate
```

**5. Crear datos de demostración**

```bash
python manage.py seed_demo
```

**6. Iniciar el servidor**

```bash
python manage.py runserver
```

**6. Abrir en el navegador**

```
http://127.0.0.1:8000/
```

---

## Rutas principales

| Ruta | Descripción | Acceso |
|---|---|---|
| `/` | Página de inicio | Público |
| `/registro/` | Crear nueva cuenta | Público |
| `/login/` | Iniciar sesión | Público |
| `/logout/` | Cerrar sesión | Autenticado |
| `/dashboard/` | Panel del usuario | **Protegida** |
| `/productos/` | Catálogo de productos desde BD | **Cliente autenticado** |
| `/carrito/` | Carrito de compras | **Cliente autenticado** |
| `/comprar/` | Confirmación de compra | **Cliente autenticado** |
| `/pedido/<id>/` | Detalle de pedido | **Cliente autenticado** |
| `/administracion/productos/` | CRUD administrativo de productos | **Staff/Admin** |
| `/admin/` | Admin nativo de Django | **Superusuario** |

> Las rutas marcadas como **Protegida** redirigen automáticamente a `/login/` si el usuario no ha iniciado sesión.

---

## Credenciales de prueba

Luego de ejecutar `python manage.py seed_demo`:

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin_demo` | `Admin12345` |
| Cliente | `cliente_demo` | `Cliente12345` |

También se puede crear un usuario desde `/registro/`.

---

## Estructura del proyecto

```
Modulo 6 - Ecommerce/
├── manage.py
├── db.sqlite3
├── ecommerce/              # Configuración del proyecto
│   ├── settings.py
│   └── urls.py
└── tienda/                 # Aplicación principal
    ├── models.py           # Categoría, Producto, Pedido y DetallePedido
    ├── views.py            # Lógica de catálogo, carrito, compra y CRUD
    ├── urls.py             # Rutas de la app
    ├── forms.py            # Formularios con validación
    ├── management/commands/seed_demo.py
    └── templates/
        └── tienda/
            ├── base.html
            ├── home.html
            ├── login.html
            ├── registro.html
            ├── dashboard.html
            ├── productos.html
            ├── carrito.html
            ├── confirmar_compra.html
            ├── detalle_pedido.html
            ├── admin_productos.html
            ├── producto_form.html
            └── producto_confirmar_eliminacion.html
```

---

## Funcionalidades implementadas

- **Login y logout** mediante el sistema de autenticación de Django
- **Registro de usuario** con validación de contraseñas (coincidencia y duplicados)
- **Vistas protegidas** con `@login_required` — redirigen a login si no hay sesión activa
- **Template base** con herencia en todas las páginas
- **Navbar dinámico** que cambia según el estado de sesión del usuario
- **Mensajes flash** para feedback de acciones (login, logout, registro)
- **Modelos ORM** para categorías, productos, pedidos y detalle de pedidos
- **Migraciones** para crear y poblar estructura inicial del catálogo
- **CRUD de productos** restringido a usuarios staff/admin
- **Catálogo persistente** cargado desde base de datos
- **Carrito de compras** basado en sesión
- **Confirmación de compra** con transacción atómica, descuento de stock y registro de pedido

## Relación con los módulos

### Módulo 7 - Acceso a datos en Django

Se implementa la capa de datos del e-commerce:

- Modelos `Categoria`, `Producto`, `Pedido` y `DetallePedido`.
- Relaciones con `ForeignKey`.
- Migraciones para sincronizar el esquema.
- Consultas ORM en vistas.
- CRUD completo de productos.

### Módulo 8 - Entrega final de portafolio

Se completa el flujo principal:

- Cliente inicia sesión.
- Cliente revisa catálogo.
- Cliente agrega productos al carrito.
- Cliente actualiza cantidades.
- Cliente confirma compra.
- El sistema crea pedido e ítems asociados al usuario.
- Administrador gestiona productos desde un área protegida.

## Pruebas

```bash
python manage.py test tienda
```

Cobertura incluida:

- Catálogo protegido por login.
- Flujo cliente: agregar al carrito y confirmar compra.
- Flujo admin: crear productos.
- Restricción de acceso a CRUD admin.

---

## Evidencia

### Registro de usuario
![alt text](<<img width="1279" height="709" alt="Captura de pantalla 2026-05-16 a la(s) 2 47 46 p m" src="https://github.com/user-attachments/assets/12a476c3-6f3a-457f-a935-873af75b5fbb" />
>)

### Inicio de sesión
![alt text](<<img width="1280" height="708" alt="Captura de pantalla 2026-05-16 a la(s) 2 48 43 p m" src="https://github.com/user-attachments/assets/6c52940f-db0b-4e50-8d73-83dcc15b9046" />
>)
### Acceso a vista protegida
![alt text](<<img width="1272" height="711" alt="Captura de pantalla 2026-05-16 a la(s) 2 50 25 p m" src="https://github.com/user-attachments/assets/3668ddc7-a4c8-4c7e-86d2-b9213a800bf9" />
>)
