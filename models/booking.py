from pydantic import BaseModel, Field


class BookingDates(BaseModel):
    checkin: str
    checkout: str


class Booking(BaseModel):
    first_name: str = Field(alias="firstname")
    last_name: str = Field(alias="lastname")
    totalprice: int
    depositpaid: bool
    booking_dates: BookingDates = Field(alias="bookingdates")
    additional_needs: str | None = Field(default=None, alias="additionalneeds")

    model_config = {"populate_by_name": True}
