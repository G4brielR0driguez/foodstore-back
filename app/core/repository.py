"""
Repository base genérico (CRUD).
Cada módulo puede heredar de esta clase para reutilizar operaciones comunes.
"""
from typing import Generic, Type, TypeVar, List, Optional
from sqlmodel import SQLModel, Session, select

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.session.get(self.model, id)

    def get_all(self, skip: int = 0, limit: int = 20) -> List[ModelType]:
        return self.session.exec(select(self.model).offset(skip).limit(limit)).all()

    def add(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        self.session.flush()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.session.delete(obj)
