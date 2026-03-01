import allure
import pytest

from config import Statuses
from tests.assertions.booking_assertions import *
from utils.booking_helpers import search_created_booking_in_bookings
from client.booking_client import BookingClient


class TestBooking:
    @allure.suite("Tests for Restful-Booker")
    @allure.title("Test that get_all_booking_ids returns status 200")
    def test_get_all_booking_ids_returns_200(self, client: BookingClient):
        response_obj = client.get_all_booking_ids()

        assert response_obj.status_code == Statuses.STATUS_OK, f"Status code is not {Statuses.STATUS_OK}"

    @allure.title("Test that get_all_booking_ids returns more than zero bookings")
    def test_get_all_booking_ids_returns_more_than_zero_bookings(self, client: BookingClient):
        response_obj = client.get_all_booking_ids()

        assert_that_booking_amount_greater_than_zero(response_obj.result)

    @allure.title("Test that create_new_booking returns status 200")
    def test_new_booking_returns_200(self, client: BookingClient, booking_data: dict):
        new_booking_id, response = client.create_new_booking(booking_data)

        assert response.status_code == Statuses.STATUS_OK, 'Booking is not created'

    @allure.title("Test that a new booking is available in the list of all existing bookings")
    def test_new_booking_can_be_found_in_list_of_all_bookings(self, client: BookingClient, booking_data: dict):
        new_booking_id, response = client.create_new_booking(booking_data)

        all_bookings = client.get_all_booking_ids().result
        is_new_booking_created = search_created_booking_in_bookings(all_bookings, new_booking_id)
        assert is_new_booking_created, f'Booking {new_booking_id} is not found in all bookings'

    @allure.title("Test that a specific booking contains all data specified during its creation")
    def test_new_booking_contains_all_passed_data(self, client: BookingClient, booking_data: dict):
        new_booking_id, _ = client.create_new_booking(booking_data)

        response_obj = client.get_booking_by_id(new_booking_id)
        assert response_obj.result == booking_data, 'Booking data does not match'

    @pytest.mark.parametrize(
        "api_key,new_value,booking_attr",
        [
            ("firstname", "Updated First Name", "first_name"),
            ("lastname", "Updated Last Name", "last_name"),
            ("totalprice", 999, "totalprice"),
            ("depositpaid", True, "depositpaid"),
            ("bookingdates", {"checkin": "2025-02-01", "checkout": "2025-02-05"}, "booking_dates"),
            ("additionalneeds", "Breakfast", "additional_needs"),
        ],
        ids=["firstname", "lastname", "totalprice", "depositpaid", "bookingdates", "additionalneeds"],
    )
    @allure.title("Test that a booking field can be updated")
    def test_booking_field_can_be_updated(
        self, client: BookingClient, booking_data: dict, api_key: str, new_value, booking_attr: str
    ):
        allure.dynamic.title(f"Test that {api_key} can be updated")
        new_booking_id, _ = client.create_new_booking(booking_data)

        response = client.update_booking(new_booking_id, **{api_key: new_value})
        assert response.booking is not None, "Expected a booking in response"
        if booking_attr == "booking_dates":
            assert response.booking.booking_dates.checkin == new_value["checkin"], "checkin was not updated"
            assert response.booking.booking_dates.checkout == new_value["checkout"], "checkout was not updated"
        else:
            assert getattr(response.booking, booking_attr) == new_value, f"{booking_attr} was not updated"

    @allure.title("Test that delete a booking returns status 201")
    def test_delete_booking_returns_201(self, client: BookingClient, booking_data: dict):
        new_booking_id, _ = client.create_new_booking(booking_data)
        response = client.delete_booking(new_booking_id)
        assert response.status_code == Statuses.STATUS_CREATED, f'Booking status is not {Statuses.STATUS_CREATED}, it is {response.status_code}'

    @allure.title("Test that once booking is deleted it is not available in the list of all bookings")
    def test_booking_can_be_deleted(self, client: BookingClient, booking_data: dict):
        new_booking_id, _ = client.create_new_booking(booking_data)
        client.delete_booking(new_booking_id)

        all_bookings = client.get_all_booking_ids().result
        is_booking_deleted = search_created_booking_in_bookings(all_bookings, new_booking_id)
        assert not is_booking_deleted, f'Booking {new_booking_id} is not deleted'



