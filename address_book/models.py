from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, inspect

import settings

Base = declarative_base()

engine = create_engine(f"sqlite:///{settings.DB_NAME}")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


class AsDictMixin:
    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class Address(AsDictMixin, Base):
    __tablename__ = 'address'
    id = Column(Integer, autoincrement=True, primary_key=True)

    master_address = Column(String)
    latitude = Column(String)
    longitude = Column(String)
