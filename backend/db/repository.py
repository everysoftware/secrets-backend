from abc import ABC
from collections.abc import Sequence
from typing import Any, ClassVar, TypeVar, cast

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.base.models import Entity
from backend.base.repository import IRepository
from backend.base.specification import BasicPagination, Page, Specification
from backend.base.types import UUID
from backend.db.exceptions import NoResultFound

T = TypeVar("T", bound=Entity)


class SQLAlchemyRepository(IRepository[T], ABC):
    model_type: ClassVar[type[Entity]]

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def add(self, model: T) -> T:
        self.session.add(model)
        return model

    async def get(self, ident: UUID) -> T | None:
        model = await self.session.get(self.model_type, ident)
        if model is None:
            return None
        return cast(T, model)

    async def get_one(self, ident: UUID) -> T:
        model = await self.get(ident)
        if model is None:
            raise NoResultFound()
        return model

    async def find(self, *spec: Specification) -> T | None:
        stmt = self._select(BasicPagination(limit=1), *spec)
        result = await self.session.scalars(stmt)
        return result.first()

    async def find_one(self, *spec: Specification) -> T:
        model = await self.find(*spec)
        if model is None:
            raise NoResultFound()
        return model

    async def remove(self, model: T) -> T:
        await self.session.delete(model)
        return model

    async def get_many(self, *spec: Specification) -> Page[T]:
        result = await self.session.scalars(self._select(*spec))
        return self._to_page(result.all())

    def _to_page(self, items: Sequence[Any]) -> Page[T]:
        return Page(items=items)

    def _select(self, *spec: Specification) -> Select[tuple[T]]:
        stmt = select(self.model_type)
        for s in spec:
            stmt = s.to_expression(stmt, self.model_type)
        return stmt  # type: ignore[return-value]
