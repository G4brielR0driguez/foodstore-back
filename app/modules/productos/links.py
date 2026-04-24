"""Tablas de unión (Link Models) para las relaciones M:N de Producto."""
from sqlmodel import SQLModel, Field


class ProductoCategoria(SQLModel, table=True):
    producto_id: int = Field(default=None, foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(default=None, foreign_key="categoria.id", primary_key=True)
    es_principal: bool = Field(default=False)


class ProductoIngrediente(SQLModel, table=True):
    producto_id: int = Field(default=None, foreign_key="producto.id", primary_key=True)
    ingrediente_id: int = Field(default=None, foreign_key="ingrediente.id", primary_key=True)
    es_removible: bool = Field(default=False)
