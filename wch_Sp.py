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
    name = Column(String(150), nullable=False)
    email = Column(String(250), nullable=False)


class Watchname(Base):
    __tablename__ = 'watchname'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="watchname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class Watchlist(Base):
    __tablename__ = 'watchlist'
    id = Column(Integer, primary_key=True)
    modelname = Column(String(350), nullable=False)
    description = Column(String(150))
    price = Column(String(150))
    rating = Column(String(150))
    color = Column(String(300), nullable=False)
    modelweight = Column(String(150))
    modellength = Column(String(140))
    modelwidth = Column(String(120))
    date = Column(DateTime, nullable=False)
    watchnameid = Column(Integer, ForeignKey('watchname.id'))
    watchname = relationship(
        Watchname, backref=backref('watchlist', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="watchlist")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'modelname': self.modelname,
            'description': self. description,
            'price': self. price,
            'rating': self. rating,
            'color': self.color,
            'modelweight': self.modelweight,
            'modellength': self.modellength,
            'modelwidth': self.modelwidth,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///Watches.db')
Base.metadata.create_all(engin)
