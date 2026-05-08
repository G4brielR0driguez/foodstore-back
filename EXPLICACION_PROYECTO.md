# 📘 Guía Completa: Arquitectura y Funcionamiento de FoodStore

Este documento explica paso a paso cómo está estructurado el proyecto **FoodStore**, cómo funciona cada parte y cómo se comunican el Frontend y el Backend.

---

## 🏗️ 1. Arquitectura General
El proyecto sigue un modelo **Cliente-Servidor**:
1.  **Backend (API)**: Construido con FastAPI, gestiona los datos y las reglas de negocio.
2.  **Frontend (Web)**: Construido con React + Vite, es la interfaz que usa el cliente.
3.  **Base de Datos**: PostgreSQL (gestionada a través de SQLModel/SQLAlchemy).

---

## 📂 2. Estructura del Backend (`foodstore-back`)

El backend utiliza una **Arquitectura Limpia y Modular**. En lugar de tener todos los modelos en un sitio y todas las rutas en otro, agrupamos por "módulo" (funcionalidad).

### Carpeta Raíz
- `main.py`: Punto de entrada. Configura la aplicación, los permisos (CORS) y conecta las rutas.
- `.env`: Contiene secretos y configuraciones (como la URL de la base de datos).
- `requirements.txt`: Las librerías necesarias (FastAPI, SQLModel, etc.).

### Carpeta `app/core` (El Motor)
Contiene la lógica compartida por toda la aplicación:
- **`database.py`**: Configura la conexión. `init_db` crea las tablas automáticamente al iniciar.
- **`repository.py`**: Contiene el `BaseRepository`. Es una plantilla con funciones comunes como "obtener todos", "buscar por ID" o "eliminar".
- **`unit_of_work.py`**: Implementa el patrón **Unit of Work (Unidad de Trabajo)**. Asegura que si una operación requiere varios cambios en la base de datos, todos se guarden (commit) o ninguno (rollback) si hay un error.

### Carpeta `app/modules` (El Dominio)
Aquí se divide la lógica por temas: `productos`, `categoria` e `ingredientes`. Cada uno tiene:
- **`models.py`**: Define la tabla en la base de datos (clase de Python = Tabla SQL).
- **`schemas.py`**: Define qué datos entran y salen por la API (Validación).
- **`service.py`**: **El Cerebro.** Aquí se aplican las reglas. El service usa el Repository para hablar con la base de datos.
- **`router.py`**: Define las URLs (endpoints) como `/productos/`.
- **`links.py`**: Define las relaciones (ej: qué ingredientes tiene un producto).

---

## 📂 3. Estructura del Frontend (`foodstore-front`)

El frontend es una aplicación moderna de **React** tipo SPA (Single Page Application).

### Carpeta `foodstore/src`
- **`main.tsx`**: Inicia la aplicación de React.
- **`App.tsx`**: Orquestador principal de la interfaz y las rutas visuales.
- **`api/`**: Contiene los "clientes" de la API. Aquí están las funciones que hacen las llamadas al backend (usando `axios` o `fetch`).
    - *Ejemplo*: `productos.ts` tiene la función `getProductos()` que llama a `GET /productos`.
- **`pages/`**: Cada vista principal de la aplicación (Productos, Categorías, Ingredientes).
    - Son componentes grandes que gestionan el "estado" (datos que cambian).
- **`components/`**: Piezas reutilizables como botones, formularios o tarjetas de productos.

---

## 🔄 4. Flujo Paso a Paso: ¿Qué pasa cuando haces clic en "Guardar"?

Imagina que estás en la web y creas un nuevo **Producto**:

1.  **Frontend (Page/Component)**: El usuario rellena el formulario y pulsa "Guardar".
2.  **Frontend (API Client)**: Se llama a la función en `src/api/productos.ts`. Esta envía un `POST` con los datos en formato JSON hacia el Backend.
3.  **Backend (Router)**: El archivo `router.py` del módulo productos recibe la petición. Valida que los datos sean correctos según el `schema`.
4.  **Backend (Service)**: El router le pasa la pelota al `service.py`. El service comprueba reglas (ej: "que el precio no sea negativo").
5.  **Backend (Unit of Work & Repository)**:
    - Se abre una "transacción".
    - El `Repository` guarda el producto en la base de datos.
    - Si todo sale bien, la `Unit of Work` confirma el guardado (`commit`).
6.  **Backend (Respuesta)**: El servidor devuelve un código `201 Created` y los datos del producto nuevo.
7.  **Frontend (Interfaz)**: El frontend recibe la confirmación y actualiza la lista de productos en pantalla sin necesidad de recargar toda la página.

---

## 🛠️ 5. Tecnologías Clave
- **FastAPI**: Elegido por su velocidad y por generar documentación automática (`/docs`).
- **SQLModel**: Permite usar el mismo código para validar datos y para la base de datos (unión de Pydantic y SQLAlchemy).
- **Vite**: Herramienta de construcción ultra rápida para el frontend.
- **TypeScript**: Añade "tipado" al código para evitar errores tontos de programación.

---

## 🚀 6. Cómo trabajar en el proyecto
- Si quieres **añadir un dato a la base de datos**: Modifica `models.py` y `schemas.py` en el backend.
- Si quieres **cambiar una regla de negocio**: Modifica `service.py` en el backend.
- Si quieres **cambiar algo visual**: Busca el componente en `src/components` o la página en `src/pages` en el frontend.
