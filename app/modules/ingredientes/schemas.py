"""Schemas Pydantic para Ingrediente (entrada/salida de la API)."""
from pydantic import BaseModel, Field
from typing import Optional


class IngredienteCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre único del ingrediente")
    descripcion: Optional[str] = Field(default=None, description="Descripción opcional")
    es_alergeno: bool = Field(default=False, description="Indica si el ingrediente es alérgeno")


class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    es_alergeno: Optional[bool] = None


class IngredienteRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    es_alergeno: bool

    class Config:
        from_attributes = True
