"""Router FastAPI para el módulo Categoria."""
from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Annotated, List, Optional
from fastapi import Path, Query

from app.core.database import get_session
from app.modules.categoria.schemas import CategoriaCreate, CategoriaRead, CategoriaUpdate
from app.modules.categoria.unit_of_work import CategoriaUnitOfWork
import app.modules.categoria.service as service

router = APIRouter(prefix="/categorias", tags=["Categorias"])


def get_uow(session: Session = Depends(get_session)) -> CategoriaUnitOfWork:
    return CategoriaUnitOfWork(session)


@router.get("", response_model=List[CategoriaRead], summary="Listar categorías")
def listar_categorias(
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre (parcial)")] = None,
    solo_raiz: Annotated[bool, Query(description="Solo categorías sin padre")] = False,
    skip: Annotated[int, Query(ge=0, description="Paginación: elementos a saltear")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Paginación: máximo de resultados")] = 20,
    uow: CategoriaUnitOfWork = Depends(get_uow),
):
    return service.listar_categorias(uow, nombre=nombre, solo_raiz=solo_raiz, skip=skip, limit=limit)


@router.get("/{categoria_id}", response_model=CategoriaRead, summary="Obtener categoría por ID")
def obtener_categoria(
    categoria_id: Annotated[int, Path(ge=1, description="ID de la categoría")],
    uow: CategoriaUnitOfWork = Depends(get_uow),
):
    return service.obtener_categoria(uow, categoria_id)


@router.post("", response_model=CategoriaRead, status_code=201, summary="Crear categoría")
def crear_categoria(
    datos: CategoriaCreate,
    uow: CategoriaUnitOfWork = Depends(get_uow),
):
    categoria = service.crear_categoria(uow, datos)
    uow.commit()
    uow.session.refresh(categoria)
    return categoria


@router.patch("/{categoria_id}", response_model=CategoriaRead, summary="Actualizar categoría")
def actualizar_categoria(
    categoria_id: Annotated[int, Path(ge=1, description="ID de la categoría")],
    datos: CategoriaUpdate,
    uow: CategoriaUnitOfWork = Depends(get_uow),
):
    categoria = service.actualizar_categoria(uow, categoria_id, datos)
    uow.commit()
    uow.session.refresh(categoria)
    return categoria


@router.delete("/{categoria_id}", status_code=204, summary="Eliminar categoría")
def eliminar_categoria(
    categoria_id: Annotated[int, Path(ge=1, description="ID de la categoría")],
    uow: CategoriaUnitOfWork = Depends(get_uow),
):
    service.eliminar_categoria(uow, categoria_id)
    uow.commit()
