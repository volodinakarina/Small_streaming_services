from typing import Generic, TypeVar, Type, Any

from flask import current_app
from sqlalchemy import desc
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound
from project.setup.db.models import Base

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    __model__ = Base

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> T | None:
        return self._db_session.query(self.__model__).get(pk)

    def get_all(self, page: int | None, status: str | None) -> list[Any] | list[Type[Base]] | Any:
        stmt = self._db_session.query(self.__model__)
        if status == 'new':
            if page:
                try:
                    return stmt.order_by(desc(self.__model__.year)).paginate(page=page,
                                                                             per_page=self._items_per_page).items
                except NotFound:
                    return []
            return stmt.order_by(desc(self.__model__.year)).all()
        if page:
            try:
                return stmt.paginate(page=page, per_page=self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()
