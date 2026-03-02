import allure
import pytest

from config import Statuses
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

        assert response_obj.booking_ids is not None, "Expected booking_ids list"
        assert len(response_obj.booking_ids) > 0, "Expected at least one booking"

    @allure.title("Test that get_all_booking_ids returns a list of objects with bookingid")
    def test_get_all_booking_ids_response_body_structure(self, client: BookingClient):
        response_obj = client.get_all_booking_ids()

        assert response_obj.booking_ids is not None, "Expected booking_ids list"
        assert len(response_obj.booking_ids) > 0, "Expected at least one booking ID"
        for item in response_obj.booking_ids:
            assert isinstance(item.booking_id, int), f"booking_id should be int, got {type(item.booking_id)}"

    @allure.title("Test that a booking response has expected structure (fields and types)")
    def test_booking_structure(self, client: BookingClient, booking_data: dict):
        new_booking_id, _ = client.create_new_booking(booking_data)
        response_obj = client.get_booking_by_id(new_booking_id)

        assert response_obj.booking is not None, "Expected a booking in response"
        booking = response_obj.booking
        assert isinstance(booking.first_name, str), "first_name should be str"
        assert isinstance(booking.last_name, str), "last_name should be str"
        assert isinstance(booking.total_price, int), "total_price should be int"
        assert isinstance(booking.deposit_paid, bool), "deposit_paid should be bool"
        assert booking.booking_dates is not None, "booking_dates should be present"
        assert isinstance(booking.booking_dates.check_in, str), "booking_dates.check_in should be str"
        assert isinstance(booking.booking_dates.check_out, str), "booking_dates.check_out should be str"

    @allure.title("Test that create_new_booking returns status 200")
    def test_new_booking_returns_200(self, client: BookingClient, booking_data: dict):
        new_booking_id, response = client.create_new_booking(booking_data)

        assert response.status_code == Statuses.STATUS_OK, 'Booking is not created'

    @allure.title("Test that a new booking is available in the list of all existing bookings")
    def test_new_booking_can_be_found_in_list_of_all_bookings(self, client: BookingClient, booking_data: dict):
        new_booking_id, response = client.create_new_booking(booking_data)

        all_bookings_response = client.get_all_booking_ids()
        assert all_bookings_response.booking_ids is not None, "Expected booking_ids list"
        is_new_booking_created = search_created_booking_in_bookings(all_bookings_response.booking_ids, new_booking_id)
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
            ("totalprice", 999, "total_price"),
            ("depositpaid", True, "deposit_paid"),
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
            assert response.booking.booking_dates.check_in == new_value["checkin"], "check_in was not updated"
            assert response.booking.booking_dates.check_out == new_value["checkout"], "check_out was not updated"
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

        all_bookings_response = client.get_all_booking_ids()
        assert all_bookings_response.booking_ids is not None, "Expected booking_ids list"
        is_booking_deleted = search_created_booking_in_bookings(all_bookings_response.booking_ids, new_booking_id)
        assert not is_booking_deleted, f'Booking {new_booking_id} is not deleted'

    @allure.title("Test that getting a non-existent booking returns 404")
    def test_get_nonexistent_booking_returns_404(self, client: BookingClient):
        response = client.get_booking_by_id(999999999)

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        assert response.is_client_error, "Expected client error (4xx)"
        assert not response.response_valid, "Response should not be valid for 404"

    @allure.title("Test that updating without auth token returns 403")
    def test_update_without_token_returns_403(self, client: BookingClient, booking_data: dict):
        new_booking_id, _ = client.create_new_booking(booking_data)
        client.token = None

        response = client.update_booking(new_booking_id, firstname="Unauthorized")

        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        assert response.is_client_error, "Expected client error (4xx)"
        assert response.error_message is not None, "Expected error message to be captured"



