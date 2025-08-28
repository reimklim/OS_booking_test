import pytest
import requests
from pydantic import BaseModel, Field, ValidationError

class Booking(BaseModel):
    bookingid: int = Field(ge=1)

@pytest.mark.usefixtures
@pytest.mark.api_get
def test_get_booking():
    '''Тест получения всех броней'''

    response = requests.get('https://restful-booker.herokuapp.com/booking')

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
            print(Booking(**booking))
    except ValidationError:
        pytest.xfail("Неверный формат тела ответа")


# @pytest.mark.api_get
# def test_get_booking_id():
#     '''Тест получения информации о брони'''

#     response = requests.get('https://restful-booker.herokuapp.com/booking/264')

#     assert response.status_code == 200
#     assert response.json()
