"""Modelo SQLModel para la tabla Ingrediente."""
from sqlmodel import SQLModel, Field
from typing import Optional


class Ingrediente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, max_length=100)
    descripcion: Optional[str] = None
    es_alergeno: bool = Field(default=False)
