"""Repository para operaciones de base de datos de Categoria."""
from typing import List, Optional
from sqlmodel import Session, select
from app.modules.categoria.models import Categoria
from app.core.repository import BaseRepository


class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session):
        super().__init__(Categoria, session)

    def get_by_nombre(self, nombre: str) -> Optional[Categoria]:
        return self.session.exec(
            select(Categoria).where(Categoria.nombre == nombre)
        ).first()

    def get_filtered(
        self,
        nombre: Optional[str] = None,
        solo_raiz: bool = False,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Categoria]:
        query = select(Categoria)
        if nombre:
            query = query.where(Categoria.nombre.ilike(f"%{nombre}%"))
        if solo_raiz:
            query = query.where(Categoria.parent_id == None)
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()
