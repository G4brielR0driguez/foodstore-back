"""Unit of Work para Producto."""
from sqlmodel import Session
from app.core.unit_of_work import UnitOfWork
from app.modules.productos.repository import ProductoRepository
from app.modules.categoria.repository import CategoriaRepository
from app.modules.ingredientes.repository import IngredienteRepository


class ProductoUnitOfWork(UnitOfWork):
    def __init__(self, session: Session):
        super().__init__(session)
        self.productos = ProductoRepository(session)
        self.categorias = CategoriaRepository(session)
        self.ingredientes = IngredienteRepository(session)
