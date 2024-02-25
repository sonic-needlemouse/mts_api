from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from .books import ReturnedBook

__all__ = ["IncomingSeller", "ReturnedSeller", "ReturnedAllSellers"]

# Базовый класс "Продавцы", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str

# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    first_name: str = "John"  # Пример присваивания дефолтного значения
    last_name: str = "Ivanov"
    email: str = "Ivanov_John@mail.ru"
    password: str = "123456_qwerty"
    # password: str

# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedSeller(BaseSeller):
    id: int

class ReturnedSellerBooks(BaseSeller):
    books: list[ReturnedBook]


# Класс для возврата массива Продавцов
class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]
