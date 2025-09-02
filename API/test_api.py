import pytest
import requests
from pydantic import BaseModel, Field, ValidationError
from datetime import date

new_booking_id = []

class BookingGetResponse(BaseModel):
    bookingid: int = Field(ge=1)

class BookingDates(BaseModel):
    checkin: date
    checkout: date

class BookingGetForId(BaseModel):
    firstname: str
    lastname: str
    totalprice: float
    depositpaid: bool
    bookingdates: BookingDates



@pytest.mark.usefixtures("base_url")
@pytest.mark.api_get
def test_get_booking(base_url):
    '''Тест получения всех броней'''

    response = requests.get(f"{base_url}/booking")

    # Проверка на успешный ответ
    try:
        assert response.status_code == 200
    except AssertionError:
        pytest.xfail("Баг: Сервер возвращает 400 вместо 200 на запрос списка броней")

    # Проверка на пустой список
    data = response.json()
    try:
        assert len(data) > 0
    except AssertionError:
        pytest.xfail("Баг: Сервер возвращает пустой список броней")

   # Проверка корректности формата тела ответа
    try:
        for booking in data:
            BookingGetResponse(**booking)
    except ValidationError:
        pytest.xfail("Неверный формат тела ответа")



@pytest.mark.usefixtures("base_url")
@pytest.mark.api_post
@pytest.mark.parametrize("firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds", [
    ("Sally", "Brown", 111, True, "2013-02-23", "2014-10-23", "Breakfast"),
    ("Josh", "Allen", 150.5, False, "2018-01-01", "2019-01-01", "super bowls"),
    ("John", "Smith", 0, True, "2020-06-15", "2020-06-20", None),
    ("Anna", "Ivanova", 42, False, "2024-12-01", "2024-12-05", "Late checkout"),
    ("Мария", "Петрова", 75.25, True, "2025-01-10", "2025-01-15", "Завтрак"),
    ("Edge", "Case", 9999999, True, "1970-01-01", "2100-12-31", ""),
    ("Short", "Stay", 10, False, "2025-08-01", "2025-08-01", "None"),
])
def test_create_booking(base_url, firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds):
    '''Тест добавления новой брони'''

    response = requests.post(f"{base_url}/booking", json={
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {
            "checkin": checkin,
            "checkout": checkout
        },
        "additionalneeds": additionalneeds
    })

    data = dict(response.json())
    new_booking_id.append(data.get("bookingid"))

    try:
        assert response.status_code == 200
        print(new_booking_id)
    except AssertionError:
        pytest.xfail("Баг: Север не возвращает успех при создании брони с корректными данными")



@pytest.mark.usefixtures("base_url")
@pytest.mark.api_get
def test_get_booking_id(base_url, created_booking_ids):
    '''Тест получения броней по ID'''
    
    for booking_id in created_booking_ids:
        response = requests.get(f"{base_url}/booking/{booking_id}")
        assert response.status_code == 200, f"Бронь {booking_id} недоступна"
        
        try:
            BookingGetForId(**response.json())
        except ValidationError as e:
            pytest.fail(f"Неверный формат для брони {booking_id}: {e}")
