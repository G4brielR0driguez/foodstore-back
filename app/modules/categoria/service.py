"""Lógica de negocio para Categoria."""
from typing import List, Optional
from fastapi import HTTPException
from app.modules.categoria.models import Categoria
from app.modules.categoria.schemas import CategoriaCreate, CategoriaUpdate
from app.modules.categoria.unit_of_work import CategoriaUnitOfWork


def listar_categorias(
    uow: CategoriaUnitOfWork,
    nombre: Optional[str] = None,
    solo_raiz: bool = False,
    skip: int = 0,
    limit: int = 20,
) -> List[Categoria]:
    return uow.categorias.get_filtered(nombre=nombre, solo_raiz=solo_raiz, skip=skip, limit=limit)


def obtener_categoria(uow: CategoriaUnitOfWork, categoria_id: int) -> Categoria:
    cat = uow.categorias.get_by_id(categoria_id)
    if not cat:
        raise HTTPException(status_code=404, detail=f"Categoría con id={categoria_id} no encontrada")
    return cat


def crear_categoria(uow: CategoriaUnitOfWork, datos: CategoriaCreate) -> Categoria:
    if uow.categorias.get_by_nombre(datos.nombre):
        raise HTTPException(status_code=400, detail=f"Ya existe una categoría con el nombre '{datos.nombre}'")
    if datos.parent_id is not None and not uow.categorias.get_by_id(datos.parent_id):
        raise HTTPException(status_code=404, detail=f"Categoría padre con id={datos.parent_id} no encontrada")

    categoria = Categoria(**datos.model_dump())
    return uow.categorias.add(categoria)


def actualizar_categoria(
    uow: CategoriaUnitOfWork,
    categoria_id: int,
    datos: CategoriaUpdate,
) -> Categoria:
    cat = uow.categorias.get_by_id(categoria_id)
    if not cat:
        raise HTTPException(status_code=404, detail=f"Categoría con id={categoria_id} no encontrada")

    if datos.nombre is not None and datos.nombre != cat.nombre:
        if uow.categorias.get_by_nombre(datos.nombre):
            raise HTTPException(status_code=400, detail=f"Ya existe una categoría con el nombre '{datos.nombre}'")

    if datos.parent_id is not None:
        if datos.parent_id == categoria_id:
            raise HTTPException(status_code=400, detail="Una categoría no puede ser su propio padre")
        if not uow.categorias.get_by_id(datos.parent_id):
            raise HTTPException(status_code=404, detail=f"Categoría padre con id={datos.parent_id} no encontrada")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(cat, campo, valor)

    uow.session.add(cat)
    uow.session.flush()
    uow.session.refresh(cat)
    return cat


def eliminar_categoria(uow: CategoriaUnitOfWork, categoria_id: int) -> None:
    cat = uow.categorias.get_by_id(categoria_id)
    if not cat:
        raise HTTPException(status_code=404, detail=f"Categoría con id={categoria_id} no encontrada")
    uow.categorias.delete(cat)
