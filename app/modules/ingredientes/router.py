"""Router FastAPI para el módulo Ingredientes."""
from fastapi import APIRouter, Depends, Path, Query
from sqlmodel import Session
from typing import Annotated, List, Optional

from app.core.database import get_session
from app.modules.ingredientes.schemas import IngredienteCreate, IngredienteRead, IngredienteUpdate
from app.modules.ingredientes.unit_of_work import IngredienteUnitOfWork
import app.modules.ingredientes.service as service

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


def get_uow(session: Session = Depends(get_session)) -> IngredienteUnitOfWork:
    return IngredienteUnitOfWork(session)


@router.get("", response_model=List[IngredienteRead], summary="Listar ingredientes")
def listar_ingredientes(
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre (parcial)")] = None,
    solo_alergenos: Annotated[bool, Query(description="Solo alérgenos")] = False,
    skip: Annotated[int, Query(ge=0, description="Paginación: elementos a saltear")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Paginación: máximo de resultados")] = 20,
    uow: IngredienteUnitOfWork = Depends(get_uow),
):
    return service.listar_ingredientes(uow, nombre=nombre, solo_alergenos=solo_alergenos, skip=skip, limit=limit)


@router.get("/{ingrediente_id}", response_model=IngredienteRead, summary="Obtener ingrediente por ID")
def obtener_ingrediente(
    ingrediente_id: Annotated[int, Path(ge=1, description="ID del ingrediente")],
    uow: IngredienteUnitOfWork = Depends(get_uow),
):
    return service.obtener_ingrediente(uow, ingrediente_id)


@router.post("", response_model=IngredienteRead, status_code=201, summary="Crear ingrediente")
def crear_ingrediente(
    datos: IngredienteCreate,
    uow: IngredienteUnitOfWork = Depends(get_uow),
):
    ing = service.crear_ingrediente(uow, datos)
    uow.commit()
    uow.session.refresh(ing)
    return ing


@router.patch("/{ingrediente_id}", response_model=IngredienteRead, summary="Actualizar ingrediente")
def actualizar_ingrediente(
    ingrediente_id: Annotated[int, Path(ge=1, description="ID del ingrediente")],
    datos: IngredienteUpdate,
    uow: IngredienteUnitOfWork = Depends(get_uow),
):
    ing = service.actualizar_ingrediente(uow, ingrediente_id, datos)
    uow.commit()
    uow.session.refresh(ing)
    return ing


@router.delete("/{ingrediente_id}", status_code=204, summary="Eliminar ingrediente")
def eliminar_ingrediente(
    ingrediente_id: Annotated[int, Path(ge=1, description="ID del ingrediente")],
    uow: IngredienteUnitOfWork = Depends(get_uow),
):
    service.eliminar_ingrediente(uow, ingrediente_id)
    uow.commit()
