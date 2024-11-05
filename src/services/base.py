from typing import TypeVar, Generic

from crud.base import BaseCRUD

T = TypeVar('T', bound=BaseCRUD)


class BaseService(Generic[T]):
    def __init__(self, crud: T):
        self.crud = crud
