from pydantic import BaseModel, Field


class BookingIdItem(BaseModel):
    """Single item from get_all_booking_ids() response."""
    booking_id: int = Field(alias="bookingid")

    model_config = {"populate_by_name": True}


class BookingDates(BaseModel):
    check_in: str = Field(alias="checkin")
    check_out: str = Field(alias="checkout")

    model_config = {"populate_by_name": True}


class Booking(BaseModel):
    first_name: str = Field(alias="firstname")
    last_name: str = Field(alias="lastname")
    total_price: int = Field(alias="totalprice")
    deposit_paid: bool = Field(alias="depositpaid")
    booking_dates: BookingDates = Field(alias="bookingdates")
    additional_needs: str | None = Field(default=None, alias="additionalneeds")

    model_config = {"populate_by_name": True}
