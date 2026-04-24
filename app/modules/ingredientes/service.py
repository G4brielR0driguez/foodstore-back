"""Lógica de negocio para Ingrediente."""
from typing import List, Optional
from fastapi import HTTPException
from app.modules.ingredientes.models import Ingrediente
from app.modules.ingredientes.schemas import IngredienteCreate, IngredienteUpdate
from app.modules.ingredientes.unit_of_work import IngredienteUnitOfWork


def listar_ingredientes(
    uow: IngredienteUnitOfWork,
    nombre: Optional[str] = None,
    solo_alergenos: bool = False,
    skip: int = 0,
    limit: int = 20,
) -> List[Ingrediente]:
    return uow.ingredientes.get_filtered(nombre=nombre, solo_alergenos=solo_alergenos, skip=skip, limit=limit)


def obtener_ingrediente(uow: IngredienteUnitOfWork, ingrediente_id: int) -> Ingrediente:
    ing = uow.ingredientes.get_by_id(ingrediente_id)
    if not ing:
        raise HTTPException(status_code=404, detail=f"Ingrediente con id={ingrediente_id} no encontrado")
    return ing


def crear_ingrediente(uow: IngredienteUnitOfWork, datos: IngredienteCreate) -> Ingrediente:
    if uow.ingredientes.get_by_nombre(datos.nombre):
        raise HTTPException(status_code=400, detail=f"Ya existe un ingrediente con el nombre '{datos.nombre}'")
    ingrediente = Ingrediente(**datos.model_dump())
    return uow.ingredientes.add(ingrediente)


def actualizar_ingrediente(
    uow: IngredienteUnitOfWork,
    ingrediente_id: int,
    datos: IngredienteUpdate,
) -> Ingrediente:
    ing = uow.ingredientes.get_by_id(ingrediente_id)
    if not ing:
        raise HTTPException(status_code=404, detail=f"Ingrediente con id={ingrediente_id} no encontrado")

    if datos.nombre is not None and datos.nombre != ing.nombre:
        if uow.ingredientes.get_by_nombre(datos.nombre):
            raise HTTPException(status_code=400, detail=f"Ya existe un ingrediente con el nombre '{datos.nombre}'")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(ing, campo, valor)

    uow.session.add(ing)
    uow.session.flush()
    uow.session.refresh(ing)
    return ing


def eliminar_ingrediente(uow: IngredienteUnitOfWork, ingrediente_id: int) -> None:
    ing = uow.ingredientes.get_by_id(ingrediente_id)
    if not ing:
        raise HTTPException(status_code=404, detail=f"Ingrediente con id={ingrediente_id} no encontrado")
    uow.ingredientes.delete(ing)
