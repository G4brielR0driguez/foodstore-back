from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.database import init_db
from app.modules.categoria.router import router as categorias_router
from app.modules.ingredientes.router import router as ingredientes_router
from app.modules.productos.router import router as productos_router

app = FastAPI(
    title="FoodStore API",
    description="API del parcial de Programación 4 — Catálogo de productos",
    version="1.0.0",
    redirect_slashes=False,
)

# Inicializar base de datos
init_db()

# Registrar routers
app.include_router(categorias_router)
app.include_router(ingredientes_router)
app.include_router(productos_router)


@app.get("/", include_in_schema=False)
def root():
    """Redirige automáticamente a la documentación interactiva."""
    return RedirectResponse(url="/docs")
