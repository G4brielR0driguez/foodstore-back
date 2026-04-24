"""Repository para operaciones de base de datos de Producto."""
from typing import List, Optional
from sqlmodel import Session, select
from app.modules.productos.models import Producto
from app.modules.productos.links import ProductoCategoria, ProductoIngrediente
from app.core.repository import BaseRepository


class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session):
        super().__init__(Producto, session)

    def get_filtered(
        self,
        nombre: Optional[str] = None,
        disponible: Optional[bool] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Producto]:
        query = select(Producto)
        if nombre:
            query = query.where(Producto.nombre.ilike(f"%{nombre}%"))
        if disponible is not None:
            query = query.where(Producto.disponible == disponible)
        if precio_min is not None:
            query = query.where(Producto.precio_base >= precio_min)
        if precio_max is not None:
            query = query.where(Producto.precio_base <= precio_max)
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()

    def get_links_categoria(self, producto_id: int) -> List[ProductoCategoria]:
        return self.session.exec(
            select(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)
        ).all()

    def get_links_ingrediente(self, producto_id: int) -> List[ProductoIngrediente]:
        return self.session.exec(
            select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)
        ).all()
