import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(300))


class AcBrandName(Base):
    __tablename__ = 'acbrandname'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="acbrandname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class AcName(Base):
    __tablename__ = 'acname'
    id = Column(Integer, primary_key=True)
    name = Column(String(350), nullable=False)
    year = Column(String(150))
    color = Column(String(150))
    capacity = Column(String(350))
    rating = Column(String(150))
    price = Column(String(100))
    acmodel = Column(String(250))
    date = Column(DateTime, nullable=False)
    acbrandnameid = Column(Integer, ForeignKey('acbrandname.id'))
    acbrandname = relationship(
        AcBrandName, backref=backref('acname', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="acname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self. name,
            'year': self. year,
            'color': self. color,
            'capacity': self.capacity,
            'rating': self. rating,
            'price': self. price,
            'acmodel': self. acmodel,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///acs.db')
Base.metadata.create_all(engin)
