"""Modelo SQLModel para la tabla Categoria."""
from sqlmodel import SQLModel, Field
from typing import Optional


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    nombre: str = Field(unique=True, max_length=100)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
