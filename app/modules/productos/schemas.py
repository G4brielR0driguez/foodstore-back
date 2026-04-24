"""Schemas Pydantic para Producto (entrada/salida de la API)."""
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal

from app.modules.categoria.schemas import CategoriaRead
from app.modules.ingredientes.schemas import IngredienteRead


class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150, description="Nombre del producto")
    descripcion: Optional[str] = Field(default=None, description="Descripción")
    precio_base: Decimal = Field(..., ge=0, description="Precio base (>= 0)")
    imagenes_url: List[str] = Field(default=[], description="Lista de URLs de imágenes")
    stock_cantidad: int = Field(default=0, ge=0, description="Cantidad en stock")
    disponible: bool = Field(default=True, description="Si está disponible para compra")
    categoria_ids: List[int] = Field(..., min_length=1, description="IDs de categorías (mínimo 1)")
    ingrediente_ids: List[int] = Field(default=[], description="IDs de ingredientes")


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Optional[Decimal] = Field(default=None, ge=0)
    imagenes_url: Optional[List[str]] = None
    stock_cantidad: Optional[int] = Field(default=None, ge=0)
    disponible: Optional[bool] = None
    categoria_ids: Optional[List[int]] = None
    ingrediente_ids: Optional[List[int]] = None


class ProductoRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio_base: Decimal
    imagenes_url: List[str]
    stock_cantidad: int
    disponible: bool
    categorias: List[CategoriaRead] = []
    ingredientes: List[IngredienteRead] = []

    class Config:
        from_attributes = True
