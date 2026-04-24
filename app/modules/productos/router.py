"""Router FastAPI para el módulo Productos."""
from fastapi import APIRouter, Depends, Path, Query
from sqlmodel import Session
from typing import Annotated, List, Optional

from app.core.database import get_session
from app.modules.productos.schemas import ProductoCreate, ProductoRead, ProductoUpdate
from app.modules.productos.unit_of_work import ProductoUnitOfWork
import app.modules.productos.service as service

router = APIRouter(prefix="/productos", tags=["Productos"])


def get_uow(session: Session = Depends(get_session)) -> ProductoUnitOfWork:
    return ProductoUnitOfWork(session)


@router.get("", response_model=List[ProductoRead], summary="Listar productos")
def listar_productos(
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre (parcial)")] = None,
    disponible: Annotated[Optional[bool], Query(description="Filtrar por disponibilidad")] = None,
    precio_min: Annotated[Optional[float], Query(ge=0, description="Precio mínimo")] = None,
    precio_max: Annotated[Optional[float], Query(ge=0, description="Precio máximo")] = None,
    skip: Annotated[int, Query(ge=0, description="Paginación: elementos a saltear")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Paginación: máximo de resultados")] = 20,
    uow: ProductoUnitOfWork = Depends(get_uow),
):
    return service.listar_productos(
        uow, nombre=nombre, disponible=disponible,
        precio_min=precio_min, precio_max=precio_max,
        skip=skip, limit=limit,
    )


@router.get("/{producto_id}", response_model=ProductoRead, summary="Obtener producto por ID")
def obtener_producto(
    producto_id: Annotated[int, Path(ge=1, description="ID del producto")],
    uow: ProductoUnitOfWork = Depends(get_uow),
):
    return service.obtener_producto(uow, producto_id)


@router.post("", response_model=ProductoRead, status_code=201, summary="Crear producto")
def crear_producto(
    datos: ProductoCreate,
    uow: ProductoUnitOfWork = Depends(get_uow),
):
    producto = service.crear_producto(uow, datos)
    uow.commit()
    uow.session.refresh(producto)
    return producto


@router.patch("/{producto_id}", response_model=ProductoRead, summary="Actualizar producto")
def actualizar_producto(
    producto_id: Annotated[int, Path(ge=1, description="ID del producto")],
    datos: ProductoUpdate,
    uow: ProductoUnitOfWork = Depends(get_uow),
):
    producto = service.actualizar_producto(uow, producto_id, datos)
    uow.commit()
    uow.session.refresh(producto)
    return producto


@router.delete("/{producto_id}", status_code=204, summary="Eliminar producto")
def eliminar_producto(
    producto_id: Annotated[int, Path(ge=1, description="ID del producto")],
    uow: ProductoUnitOfWork = Depends(get_uow),
):
    service.eliminar_producto(uow, producto_id)
    uow.commit()