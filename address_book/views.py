from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from address_book import schemas, models, crud
from address_book.address_parser import parse_address


address_router = APIRouter(prefix='/address', tags=['address book'])


def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@address_router.get('/{address_id}/', response_model=schemas.ReadAddress)
def read_address_by_id(address_id: int,
                       session: Session = Depends(get_db)):
    address = crud.read_address_by_id(session=session, address_id=address_id)
    if not address:
        return JSONResponse(status_code=404, content='No such id!')
    return schemas.ReadAddress(**address.as_dict())


@address_router.get('/', response_model=list[schemas.ReadAddress])
def read_address(latitude: str | None = None, longitude: str | None = None,
                 session: Session = Depends(get_db)):
    address_searched = schemas.SearchAddress(longitude=longitude, latitude=latitude)

    matching_addresses = crud.read_matching_addresses(session=session, address=address_searched)
    matching_addresses = [schemas.ReadAddress(**addr.as_dict()) for addr in matching_addresses]
    return matching_addresses


@address_router.post('/', response_model=schemas.ReadAddress)
def create_address(input_address: schemas.InputAddress,
                   session: Session = Depends(get_db)):
    address_parsed = parse_address(input_address.address)
    address_to_create = schemas.CreateAddress(master_address=input_address.address, latitude=address_parsed.latitude,
                                              longitude=address_parsed.longitude)
    res = crud.create_address(session=session, address=address_to_create)

    res = schemas.ReadAddress(**res.as_dict())
    return res


@address_router.patch('/{address_id}/', response_model=schemas.ReadAddress)
def update_address(address_id: int, address: schemas.InputAddress, session: Session = Depends(get_db)):
    stored_address_model = crud.read_address_by_id(session=session, address_id=address_id)
    if not stored_address_model:
        return JSONResponse(status_code=404, content='No such id!')

    stored_address_model = schemas.CreateAddress(**stored_address_model.as_dict())

    address_parsed = parse_address(address.address)
    address_to_update = schemas.CreateAddress(master_address=address.address, latitude=address_parsed.latitude,
                                              longitude=address_parsed.longitude)
    updated_item = stored_address_model.copy(update=address_to_update.dict())

    address_updated = crud.update_address(session=session, address_id=address_id, address_updated=updated_item)
    address_updated = schemas.ReadAddress(**address_updated.as_dict())
    return address_updated


@address_router.get('/{latitude}/{longitude}/{distance}/', response_model=list[schemas.ReadAddress])
def get_matching_addresses(latitude: float, longitude: float, distance: float, session: Session = Depends(get_db)):
    point_a = (latitude, longitude)
    matching_addresses = crud.read_all_addresses_in_distance(point_a=point_a, session=session, distance=distance)
    matching_addresses = [schemas.ReadAddress(**addr.as_dict()) for addr in matching_addresses]
    return matching_addresses
