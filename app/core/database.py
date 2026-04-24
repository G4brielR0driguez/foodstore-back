"""
Conexión a la base de datos usando SQLModel + SQLAlchemy.
"""
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    """Crea todas las tablas definidas en los modelos si no existen."""
    # Importamos todos los modelos para que SQLModel los registre antes de create_all
    import app.modules.categoria.models       # noqa: F401
    import app.modules.ingredientes.models    # noqa: F401
    import app.modules.productos.models       # noqa: F401
    import app.modules.productos.links        # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependencia de FastAPI que provee una sesión de base de datos por request."""
    with Session(engine) as session:
        yield session