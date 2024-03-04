"""Валидация Pydantic для продавцов"""

from pydantic import BaseModel

from .books import ReturnedBook

__all__ = ["BaseSeller", "IncomingSeller", "ReturnedSeller", "ReturnedAllSellers", "ReturnedSellerBooks"]


# Базовый класс "Продавцы", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    first_name: str
    last_name: str
    email: str
    password: str


# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedSeller(BaseSeller):
    id: int


# Класс, для возврата списка книг, которыми торгует продавец
class ReturnedSellerBooks(BaseSeller):
    books: list[ReturnedBook]


# Класс для возврата массива Продавцов
class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]
