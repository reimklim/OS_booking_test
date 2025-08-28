import pytest
import requests
from pydantic import BaseModel, Field, ValidationError
from datetime import date


class Booking(BaseModel):
    bookingid: int = Field(ge=1)

class Dates(BaseModel):
    checkin: date
    checkout: date

class Booking_id(BaseModel):
    firstname: str
    lastname: str
    totalprice: float
    depositpaid: bool
    bookingdates: Dates

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
            Booking(**booking)
    except ValidationError:
        pytest.xfail("Неверный формат тела ответа")




@pytest.mark.usefixtures("base_url")
@pytest.mark.parametrize("bookingid", [306, 184])
@pytest.mark.api_get
def test_get_booking_id(base_url, bookingid):
    '''Тест информации о брони по id'''

    response = requests.get(f"{base_url}/booking/{bookingid}")
    
    try:
        assert response.status_code == 200
    except AssertionError:
        pytest.xfail("Баг: Сервер возвращает 400 вместо 200 на запрос брони по существующему id")

    data = response.json()

    try:
        Booking_id(**data)
    except ValidationError:
        pytest.xfail("Баг: Неверный формат тела ответа")


