import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    return "https://restful-booker.herokuapp.com"


# Фикстура для хранения ID созданных броней (выполняется один раз на модуль)
@pytest.fixture(scope="module")
def created_booking_ids(base_url):
    ids = []
    test_data = [
        ("Sally", "Brown", 111, True, "2013-02-23", "2014-10-23", "Breakfast"),
        ("Josh", "Allen", 150.5, False, "2018-01-01", "2019-01-01", "super bowls"),
        ("John", "Smith", 0, True, "2020-06-15", "2020-06-20", None),
        ("Anna", "Ivanova", 42, False, "2024-12-01", "2024-12-05", "Late checkout"),
        ("Мария", "Петрова", 75.25, True, "2025-01-10", "2025-01-15", "Завтрак"),
        ("Edge", "Case", 9999999, True, "1970-01-01", "2100-12-31", ""),
        ("Short", "Stay", 10, False, "2025-08-01", "2025-08-01", "None"),
    ]
    
    for data in test_data:
        firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds = data
        response = requests.post(
            f"{base_url}/booking",
            json={
                "firstname": firstname,
                "lastname": lastname,
                "totalprice": totalprice,
                "depositpaid": depositpaid,
                "bookingdates": {"checkin": checkin, "checkout": checkout},
                "additionalneeds": additionalneeds
            }
        )
        
        # Проверяем создание брони (этот тест теперь часть фикстуры)
        assert response.status_code == 200, f"Создание брони провалилось: {response.text}"
        booking_id = response.json()["bookingid"]
        ids.append(booking_id)
    
    yield ids  # Возвращаем ID после создания всех броней
    
    # Опционально: очистка данных после тестов
    for booking_id in ids:
        requests.delete(f"{base_url}/booking/{booking_id}")