"""Schemas Pydantic para Categoria (entrada/salida de la API)."""
from pydantic import BaseModel, Field
from typing import Optional


class CategoriaCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre único de la categoría")
    descripcion: Optional[str] = Field(default=None, description="Descripción opcional")
    imagen_url: Optional[str] = Field(default=None, description="URL de imagen")
    parent_id: Optional[int] = Field(default=None, description="ID de la categoría padre (subcategoría)")


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = None


class CategoriaRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    imagen_url: Optional[str]
    parent_id: Optional[int]

    class Config:
        from_attributes = True
