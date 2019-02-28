from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from wch_Sp import *

engine = create_engine('sqlite:///Watches.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete Watchname if exisitng.
session.query(Watchname).delete()
# Delete Watchlist if exisitng.
session.query(Watchlist).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create Users1 data
User1 = User(
    name="Doredla Gayathri", email="gayathridoredla982@gmail.com")
       
session.add(User1)
session.commit()
print ("Successfully Add First User1")
# Create sample Watchnames
w1 = Watchname(
    name="Fashion Watches", 
    user_id=1)
session.add(w1)
session.commit()
w2 = Watchname(
    name="Luxuary Watches", user_id=1)
session.add(w2)
session.commit()

w3 = Watchname(
    name="Italian Design Watches", user_id=1)
session.add(w3)
session.commit()
w4 = Watchname(
    name="Automatic Watches", user_id=1)
session.add(w4)
session.commit()
w5 = Watchname(
    name="Mechanical Watches", user_id=1)
session.add(w5)
session.commit()
print("added")
# Popular Watchnames with modelnames for testing
# Using different users for Watchlist models
list1 = Watchlist(
    modelname="Fastrak",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=1,
    user_id=1)
session.add(list1)
session.commit()
list2 = Watchlist(
    modelname="Casio",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=1,
    user_id=1)
session.add(list2)
session.commit()
list3 = Watchlist(
    modelname="Sodial", description="It is suitable for hand", price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=1,
    user_id=1)
session.add(list3)
session.commit()
list4 = Watchlist(
    modelname="Rolex",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=2,
    user_id=1)
session.add(list4)
session.commit()
list5 = Watchlist(
    modelname="Fossil",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=2,
    user_id=1)
session.add(list5)
session.commit()
list6 = Watchlist(
    modelname="Titan",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=2,
    user_id=1)
session.add(list6)
session.commit()
list7 = Watchlist(
    modelname="Timex",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=3,
    user_id=1)
session.add(list7)
session.commit()
list8 = Watchlist(
    modelname="Richclub",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=3,
    user_id=1)
session.add(list8)
session.commit()
list9 = Watchlist(
    modelname="Tedbaker",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=3,
    user_id=1)
session.add(list9)
session.commit()
list10 = Watchlist(
    modelname="Apple",
    description="It is suitable for hand",                   
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=4,
    user_id=1)                                     
session.add(list10)
session.commit()
list11 = Watchlist(
    modelname="Skagen",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=4,
    user_id=1)
session.add(list11)
session.commit()
list12 = Watchlist(
    modelname="Tommyhillfygur",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=4,
    user_id=1)
session.add(list12)
session.commit()
list13 = Watchlist(
    modelname="Diesel",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=5,
    user_id=1)
session.add(list13)
session.commit()
list14 = Watchlist(
    modelname="Armaniexchange",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=1,
    user_id=1)
session.add(list14)
session.commit()
list15 = Watchlist(
    modelname="Michaelkors",
    description="It is suitable for hand",
    price="300",
    rating="good",
    color="white",
    modelweight="20g",
    modellength="120mm",
    modelwidth="100mm",
    date=datetime.datetime.now(),
    watchnameid=5,
    user_id=1)
session.add(list15)
session.commit()
print("Your watches database has been inserted!")
