"""Repository para operaciones de base de datos de Ingrediente."""
from typing import List, Optional
from sqlmodel import Session, select
from app.modules.ingredientes.models import Ingrediente
from app.core.repository import BaseRepository


class IngredienteRepository(BaseRepository[Ingrediente]):
    def __init__(self, session: Session):
        super().__init__(Ingrediente, session)

    def get_by_id(self, id: int) -> Optional[Ingrediente]:
        """Retorna el ingrediente solo si está activo."""
        return self.session.exec(
            select(Ingrediente).where(Ingrediente.id == id, Ingrediente.activo == True)
        ).first()

    def get_by_nombre(self, nombre: str) -> Optional[Ingrediente]:
        """Retorna el ingrediente por nombre solo si está activo."""
        return self.session.exec(
            select(Ingrediente).where(Ingrediente.nombre == nombre, Ingrediente.activo == True)
        ).first()

    def get_filtered(
        self,
        nombre: Optional[str] = None,
        solo_alergenos: bool = False,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Ingrediente]:
        query = select(Ingrediente).where(Ingrediente.activo == True)
        if nombre:
            query = query.where(Ingrediente.nombre.ilike(f"%{nombre}%"))
        if solo_alergenos:
            query = query.where(Ingrediente.es_alergeno == True)
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()

    def soft_delete(self, obj: Ingrediente) -> None:
        """Borrado lógico: marca activo=False en lugar de eliminar el registro."""
        obj.activo = False
        self.session.add(obj)
