"""Lógica de negocio para Producto."""
from typing import List, Optional
from fastapi import HTTPException
from app.modules.productos.models import Producto
from app.modules.productos.links import ProductoCategoria, ProductoIngrediente
from app.modules.productos.schemas import ProductoCreate, ProductoUpdate
from app.modules.productos.unit_of_work import ProductoUnitOfWork


def listar_productos(
    uow: ProductoUnitOfWork,
    nombre: Optional[str] = None,
    disponible: Optional[bool] = None,
    precio_min: Optional[float] = None,
    precio_max: Optional[float] = None,
    skip: int = 0,
    limit: int = 20,
) -> List[Producto]:
    return uow.productos.get_filtered(
        nombre=nombre, disponible=disponible,
        precio_min=precio_min, precio_max=precio_max,
        skip=skip, limit=limit,
    )


def obtener_producto(uow: ProductoUnitOfWork, producto_id: int) -> Producto:
    producto = uow.productos.get_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail=f"Producto con id={producto_id} no encontrado")
    return producto


def crear_producto(uow: ProductoUnitOfWork, datos: ProductoCreate) -> Producto:
    # Validar categorías
    if not datos.categoria_ids:
        raise HTTPException(status_code=400, detail="Debe indicar al menos una categoría")

    for cat_id in datos.categoria_ids:
        if not uow.categorias.get_by_id(cat_id):
            raise HTTPException(status_code=404, detail=f"Categoría con id={cat_id} no encontrada")

    for ing_id in datos.ingrediente_ids:
        if not uow.ingredientes.get_by_id(ing_id):
            raise HTTPException(status_code=404, detail=f"Ingrediente con id={ing_id} no encontrado")

    # Crear el producto
    datos_producto = datos.model_dump(exclude={"categoria_ids", "ingrediente_ids"})
    producto = Producto(**datos_producto)
    uow.session.add(producto)
    uow.session.flush()

    # Crear vínculos con categorías
    for i, cat_id in enumerate(datos.categoria_ids):
        uow.session.add(ProductoCategoria(
            producto_id=producto.id,
            categoria_id=cat_id,
            es_principal=(i == 0),
        ))

    # Crear vínculos con ingredientes
    for ing_id in datos.ingrediente_ids:
        uow.session.add(ProductoIngrediente(
            producto_id=producto.id,
            ingrediente_id=ing_id,
        ))

    uow.session.flush()
    uow.session.refresh(producto)
    return producto


def actualizar_producto(
    uow: ProductoUnitOfWork,
    producto_id: int,
    datos: ProductoUpdate,
) -> Producto:
    producto = uow.productos.get_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail=f"Producto con id={producto_id} no encontrado")

    # Reemplazar categorías si se enviaron
    if datos.categoria_ids is not None:
        if not datos.categoria_ids:
            raise HTTPException(status_code=400, detail="Debe haber al menos una categoría")
        for link in uow.productos.get_links_categoria(producto_id):
            uow.session.delete(link)
        for i, cat_id in enumerate(datos.categoria_ids):
            if not uow.categorias.get_by_id(cat_id):
                raise HTTPException(status_code=404, detail=f"Categoría con id={cat_id} no encontrada")
            uow.session.add(ProductoCategoria(
                producto_id=producto_id,
                categoria_id=cat_id,
                es_principal=(i == 0),
            ))

    # Reemplazar ingredientes si se enviaron
    if datos.ingrediente_ids is not None:
        for link in uow.productos.get_links_ingrediente(producto_id):
            uow.session.delete(link)
        for ing_id in datos.ingrediente_ids:
            if not uow.ingredientes.get_by_id(ing_id):
                raise HTTPException(status_code=404, detail=f"Ingrediente con id={ing_id} no encontrado")
            uow.session.add(ProductoIngrediente(
                producto_id=producto_id,
                ingrediente_id=ing_id,
            ))

    # Actualizar campos escalares
    for campo, valor in datos.model_dump(exclude_unset=True, exclude={"categoria_ids", "ingrediente_ids"}).items():
        setattr(producto, campo, valor)

    uow.session.add(producto)
    uow.session.flush()
    uow.session.refresh(producto)
    return producto


def eliminar_producto(uow: ProductoUnitOfWork, producto_id: int) -> None:
    producto = uow.productos.get_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail=f"Producto con id={producto_id} no encontrado")
    uow.productos.delete(producto)
