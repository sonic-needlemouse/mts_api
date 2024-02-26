import pytest
from fastapi import status
from sqlalchemy import select

from src.models import books, sellers


# Тест на ручку создающую продавца
@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {"first_name": "John", "last_name": "Ivanov", "email": "Ivanov_John@mail.ru", "password": "123456_qwerty"}
    response = await async_client.post("/api/v1/seller/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == {
        "id": result_data["id"],
        "first_name": "John",
        "last_name": "Ivanov",
        "email": "Ivanov_John@mail.ru",
    }


# Тест на ручку получения списка продавцов
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    # Создаем продавцов вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller_1 = sellers.Seller(
        first_name="John", last_name="Ivanov", email="Ivanov_John@mail.ru", password="123456_qwerty"
    )
    seller_2 = sellers.Seller(
        first_name="Jack", last_name="Ivanov", email="oh_my_john@mail.ru", password="1234567890_qwerty"
    )

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/seller/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["sellers"]) == 2  # Опасный паттерн! Если в БД есть данные, то тест упадет

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "sellers": [
            {
                "id": seller_1.id,
                "first_name": "John",
                "last_name": "Ivanov",
                "email": "Ivanov_John@mail.ru",
            },
            {
                "id": seller_2.id,
                "first_name": "Jack",
                "last_name": "Ivanov",
                "email": "oh_my_john@mail.ru",
            },
        ]
    }


# Тест на ручку получения одного продавца
@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    # Создаем продавцов вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller_1 = sellers.Seller(
        first_name="John", last_name="Ivanov", email="Ivanov_John@mail.ru", password="123456_qwerty"
    )
    seller_2 = sellers.Seller(
        first_name="Jack", last_name="Ivanov", email="oh_my_john@mail.ru", password="1234567890_qwerty"
    )

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    book = books.Book(author="Dostoevsky", title="Idiot", year=2000, count_pages=104, seller_id=seller_1.id)

    db_session.add(book)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/seller/{seller_1.id}")

    assert response.status_code == status.HTTP_200_OK

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        # "id": seller_1.id,
        "first_name": "John",
        "last_name": "Ivanov",
        "email": "Ivanov_John@mail.ru",
        "books": [
            {
                "id": book.id,
                "author": "Dostoevsky",
                "title": "Idiot",
                "year": 2000,
                "count_pages": 104
            }
        ],
    }


# Тест на ручку удаления продавца
@pytest.mark.asyncio
async def test_delete_book(db_session, async_client):
    # Создаем продавца вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller = sellers.Seller(
        first_name="John", last_name="Ivanov", email="Ivanov_John@mail.ru", password="123456_qwerty"
    )

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/seller/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers.Seller))
    res = all_sellers.scalars().all()
    assert len(res) == 0


# Тест на ручку обновления данных о продавце
@pytest.mark.asyncio
async def test_update_book(db_session, async_client):
    # Создаем продавца вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller = sellers.Seller(
        first_name="John", last_name="Ivanov", email="Ivanov_John@mail.ru", password="123456_qwerty"
    )

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/seller/{seller.id}",
        json={
            "id": seller.id,
            "first_name": "John",
            "last_name": "Sidorov",
            "email": "Sidorov_John@mail.ru",
            "password": "12356415_qqdacsvsbscaca",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    # Проверяем, что обновились все поля
    res = await db_session.get(sellers.Seller, seller.id)
    assert res.id == seller.id
    assert res.first_name == "John"
    assert res.last_name == "Sidorov"
    assert res.email == "Sidorov_John@mail.ru"
