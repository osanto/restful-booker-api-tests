from faker import Faker
import pytest
import requests
import allure

from client.booking_client import BookingClient
from config import Urls, UserData, reload_credentials


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
    reload_credentials()
    if not UserData.LOGIN or not UserData.PASSWORD:
        pytest.fail(
            "Auth credentials missing. Set LOGIN and PASSWORD in .env (see .env.example)."
        )
    credentials = {
        "username": UserData.LOGIN,
        "password": UserData.PASSWORD
    }
    response = requests.post(Urls.AUTH_URL, credentials)
    if not response.ok:
        pytest.fail(
            f"Auth failed: {response.status_code} {response.reason}. "
            f"Check LOGIN/PASSWORD in .env. Response: {response.text[:200]}"
        )
    try:
        response_data = response.json()
        token = response_data.get("token")
    except (ValueError, TypeError) as e:
        pytest.fail(f"Auth response is not valid JSON: {e}. Response: {response.text[:200]}")
    if not token:
        pytest.fail(
            f"Auth response has no 'token'. Check credentials. Response: {response.text[:200]}"
        )
    client = BookingClient()
    client.set_token(token)
    yield client


