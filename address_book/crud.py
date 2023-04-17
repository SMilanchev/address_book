from sqlalchemy.orm import Session
from geopy.distance import geodesic as GD

from address_book import schemas, models
from address_book.utils import filter_step_by_step


def read_address_by_id(session: Session, address_id: int) -> models.Address:
    stmt = session.query(models.Address).filter_by(id=address_id)
    return stmt.first()


def read_matching_addresses(session: Session, address: schemas.SearchAddress) -> list:
    matching_addresses = filter_step_by_step(db=session, model=models.Address,
                                             filter_params=address.dict(exclude_none=True))
    return matching_addresses


def create_address(session: Session, address: schemas.CreateAddress) -> models.Address:
    matching_address = filter_step_by_step(db=session,
                                           filter_params=address.dict(), model=models.Address)

    if matching_address:
        return matching_address[0]

    new_address = models.Address(**address.dict())

    session.add(new_address)
    session.commit()
    session.refresh(new_address)
    return new_address


def update_address(session: Session, address_id: int, address_updated: schemas.CreateAddress) -> models.Address:
    db_address = read_address_by_id(session=session, address_id=address_id)
    for field, value in address_updated.dict().items():
        setattr(db_address, field, value)
    session.commit()
    session.refresh(db_address)
    return db_address


def read_all_addresses_in_distance(session: Session, point_a: tuple, distance: float) -> list:
    all_addresses = session.query(models.Address).all()
    res = [addr for addr in all_addresses if GD(point_a, (addr.latitude, addr.longitude)).km < distance]
    return res
