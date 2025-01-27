from faker import Faker
import pytest
import requests
import allure

from client.booking_client import BookingClient
from config import Urls, UserData


fake = Faker()


def generate_booking_payload() -> dict:
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=50, max=5000),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": fake.date_between(start_date="today", end_date="+30d").isoformat(),
            "checkout": fake.date_between(start_date="+31d", end_date="+60d").isoformat()
        },
        "additionalneeds": fake.word()
    }


@pytest.fixture
@allure.title("Prepare booking data")
def booking_data():
    yield generate_booking_payload()


@pytest.fixture
@allure.title("Prepare a client object")
def client():
    credentials = {
        "username": UserData.LOGIN,
        "password": UserData.PASSWORD
    }
    response = requests.post(Urls.AUTH_URL, credentials)
    response_data = response.json()
    token = response_data['token']
    client = BookingClient()
    client.set_token(token)
    yield client


