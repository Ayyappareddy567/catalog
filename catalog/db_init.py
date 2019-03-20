from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from db_setup import *

engine = create_engine('sqlite:///acs.db')
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

# Delete acbrandname if exisitng.
session.query(AcBrandName).delete()
# Delete acname if exisitng.
session.query(AcName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
User1 = User(name="Ayyappa Reddy",
             email="bareddyayyappareddy123@gmail.com")
session.add(User1)
session.commit()
print ("Successfully Add First User")
# Create sample ac brands
Brand1 = AcBrandName(name="LLOYD",
                     user_id=1)
session.add(Brand1)
session.commit()

Brand2 = AcBrandName(name="SAMSUNG",
                     user_id=1)
session.add(Brand2)
session.commit

Brand3 = AcBrandName(name="BLUE STAR",
                     user_id=1)
session.add(Brand3)
session.commit()

Brand4 = AcBrandName(name="OGENERAL",
                     user_id=1)
session.add(Brand4)
session.commit()

Brand5 = AcBrandName(name="MITSBUSHI",
                     user_id=1)
session.add(Brand5)
session.commit()
Brand6 = AcBrandName(name="DAIKIN",
                     user_id=1)
session.add(Brand6)
session.commit()

# Populare a acs with models for testing
# Using different users for acs names year also
Name1 = AcName(name="Lloyd LS19A3FF",
               year="2015",
               color="white",
               capacity="1 ton",
               rating="5 star",
               price="50,650",
               acmodel="split",
               date=datetime.datetime.now(),
               acbrandnameid=1,
               user_id=1)
session.add(Name1)
session.commit()

Name2 = AcName(name="SAMSUNG 25TH67GH",
               year="2018",
               color="white",
               capacity="0.75 ton",
               rating="3 star",
               price="29,650",
               acmodel="split",
               date=datetime.datetime.now(),
               acbrandnameid=2,
               user_id=1)
session.add(Name2)
session.commit()

Name3 = AcName(name="BLUE 97DT3KG STAR",
               year="2017",
               color="red",
               capacity="1.5 ton",
               rating="3 star",
               price="39,650",
               acmodel="split",
               date=datetime.datetime.now(),
               acbrandnameid=3,
               user_id=1)
session.add(Name3)
session.commit()

Name4 = AcName(name="ASGA 24",
               year="2014",
               color="blue",
               capacity="1 ton",
               rating="5 star",
               price="32,650",
               acmodel="window",
               date=datetime.datetime.now(),
               acbrandnameid=4,
               user_id=1)
session.add(Name4)
session.commit()

Name5 = AcName(name="MITSHBUSHI MTSB23",
               year="2011",
               color="white",
               capacity="1 ton",
               rating="5 star",
               price="27,650",
               acmodel="window",
               date=datetime.datetime.now(),
               acbrandnameid=5,
               user_id=1)
session.add(Name5)
session.commit()

Name6 = AcName(name="DAIKIN DL2C36DN",
               year="2010",
               color="white",
               capacity="1.5 ton",
               rating="3 star",
               price="47,650",
               acmodel="split",
               date=datetime.datetime.now(),
               acbrandnameid=6,
               user_id=1)
session.add(Name6)
session.commit()


print("Your acs database has been inserted!")
