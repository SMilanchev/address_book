from pydantic import BaseModel, validator
from address_book.address_parser import parse_address


class Address(BaseModel):
    master_address: str
    latitude: str
    longitude: str


class CreateAddress(Address):
    pass


class ReadAddress(Address):
    id: int


class InputAddress(BaseModel):
    address: str

    @validator('address')
    def address_exists(cls, value):
        loc = parse_address(value)
        if loc:
            return value

        raise ValueError(f'{value} not valid address!')


class SearchAddress(BaseModel):
    latitude: str | None
    longitude: str | None
