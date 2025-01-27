from json import dumps
from typing import Optional, Tuple

import requests

from client.base_client import BaseClient
from utils.booking_response import Response
from config import Urls, Logging

logger = Logging.setup_logging()


class BookingClient(BaseClient):
    def __init__(self):
        super().__init__()

        self.token: Optional[str] = None
        self.base_url: str = Urls.BASE_URL
        self.auth_url: str = Urls.AUTH_URL

    def set_token(self, token: str) -> None:
        self.token = token

    def get_headers(self, with_token: bool) -> dict[str, str]:
        if not with_token:
            return self.headers

        headers = self.headers.copy()
        headers["Cookie"] = f'token={self.token}'
        return headers

    def get_all_booking_ids(self) -> Response:
        response_obj = Response(requests.get(self.base_url, headers=self.get_headers(with_token=False)))
        if response_obj.result is None:
            logger.error("Failed to get a response from the bookings service. Response is None.")
            raise ValueError("No response received from the bookings service.")
        logger.info(f"Getting all bookings ids. "
                    f"Status code: {response_obj.status_code}. ")
        return response_obj

    def get_booking_by_id(self, booking_id: int) -> Response:
        url = f'{self.base_url}/{booking_id}'
        response_obj = Response(requests.get(url, headers=self.get_headers(with_token=False)))
        logger.info(f"Getting booking by ID: {booking_id}. Status code: {response_obj.status_code}.")

        if response_obj.response_valid:
            logger.info(f"Successfully retrieved booking. Full response: {response_obj.result}")
        else:
            logger.error(f"Failed to retrieve booking. Status code: {response_obj.status_code}. "
                         f"Full response: {response_obj.result if response_obj.result else 'No response data'}")

        return response_obj

    def create_new_booking(self, booking_data: str) -> Tuple[int, Response]:
        payload = dumps(booking_data)

        try:
            raw_response = requests.post(self.base_url, data=payload, headers=self.get_headers(with_token=False))
            response = Response(raw_response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create a new booking. Error: {e}. Payload: {payload}")
            raise

        if not response.response_valid:
            logger.error(
                f"Invalid response received. Status code: {response.status_code}, Response: {raw_response.text}")
            raise ValueError(f"Invalid response received: {raw_response.text}")

        booking_id = response.result["bookingid"]
        if booking_id is None:
            logger.error(f"Booking ID missing in response: {response.result}")
            raise ValueError("Booking ID is missing from the response")

        logger.info(f"New booking created successfully. Status code: {response.status_code}. "
                    f"Booking ID: {booking_id}, ")

        return booking_id, response

    def update_booking_first_name(self, booking_id: str, first_name: str) -> Response:
        url = f'{self.base_url}/{booking_id}'
        payload = self.__generate_booking_payload_first_name(first_name)
        response_obj = Response(requests.patch(url, data=payload, headers=self.get_headers(with_token=True)))

        logger.info(f"Updating booking ID {booking_id} with first name: {first_name}. "
                    f"Status code: {response_obj.status_code}.")

        if response_obj.response_valid:
            logger.info(f"Successfully updated booking. Full response: {response_obj.result}")
        else:
            logger.error(f"Failed to update booking ID {booking_id}. Status code: {response_obj.status_code}. "
                         f"Full response: {response_obj.result if response_obj.result else 'No response data'}")

        return response_obj

    def delete_booking(self, booking_id: str) -> Response:
        url = f'{self.base_url}/{booking_id}'
        response_obj = Response(requests.delete(url, headers=self.get_headers(with_token=True)))

        logger.info(f"Deleting booking ID {booking_id}. Status code: {response_obj.status_code}.")

        if response_obj.status_code == 201:
            logger.info(f"Successfully deleted booking ID {booking_id}. Full response: {response_obj.result}")
        else:
            logger.error(f"Failed to delete booking ID {booking_id}. Status code: {response_obj.status_code}. "
                         f"Full response: {response_obj.result if response_obj.result else 'No response data'}")

        return response_obj

    @staticmethod
    def __generate_booking_payload_first_name(first_name: str) -> str:
        return dumps({"firstname": first_name})
