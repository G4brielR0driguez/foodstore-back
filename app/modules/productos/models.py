"""Modelo SQLModel para la tabla Producto."""
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import String
from typing import Optional, List
from decimal import Decimal

from app.modules.productos.links import ProductoCategoria, ProductoIngrediente
from app.modules.categoria.models import Categoria
from app.modules.ingredientes.models import Ingrediente


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=150)
    descripcion: Optional[str] = None
    precio_base: Decimal = Field(default=Decimal("0.00"), ge=0)
    imagenes_url: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)

    categorias: List[Categoria] = Relationship(link_model=ProductoCategoria)
    ingredientes: List[Ingrediente] = Relationship(link_model=ProductoIngrediente)
