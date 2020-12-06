import pandas as pd
from sodapy import Socrata
from config.py import APP_TOKEN, EMAIL, PASSWORD

client = Socrata("data.cityofnewyork.us",
                 APP_TOKEN,
                 username=EMAIL,
                 password=PASSWORD)

babies_ept = "25th-nujf"
doggos_ept = "nu7n-tubp"

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect, Column, Integer, String

engine = create_engine("sqlite:///db/doggo-db.sqlite")

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Baby(Base):
    __tablename__ = 'babies'
    
    id = Column(Integer, primary_key=True)
    brth_yr = Column(Integer)
    gndr = Column(String)
    ethcty = Column(String)
    nm = Column(String)
    cnt = Column(Integer)
    rnk = Column(Integer)
    
    def __repr__(self):
        return "<Baby(brth_yr='%s', gndr='%s', ethcty='%s', nm='%s', cnt='%s', rnk='%s')>" % (
                        self.brth_yr, self.gndr, self.ethcty, self.nm, self.cnt, self.rnk)

class Doggo(Base):
    __tablename__ = 'doggos'
    
    id = Column(Integer, primary_key=True)
    rownumber = Column(Integer)
    animalname = Column(String)
    animalgender = Column(String)
    animalbirth = Column(Integer)
    breedname = Column(String)
    zipcode = Column(String)
    licenseissueddate = Column(String)
    licenseexpireddate = Column(String)
    extract_year = Column(Integer)
    
    def __repr__(self):
        return "<Doggo(rownumber='%s', animalname='%s', animalgender='%s', animalbirth='%s', breedname='%s', zipcode='%s', licenseissueddate='%s', licenseexpireddate='%s', extract_year='%s')>" % (
                        self.rownumber, self.animalname, self.animalgender, self.animalbirth, self.breedname, self.zipcode, self.licenseissueddate, self.licenseexpireddate, self.extract_year)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

babies = client.get(babies_ept, limit=1000000000)
doggos = client.get(doggos_ept, limit=1000000000)

for baby in babies:
    new_baby = Baby(brth_yr = baby['brth_yr'],
                    gndr = baby['gndr'],
                    ethcty = baby['ethcty'],
                    nm = baby['nm'],
                    cnt = baby['cnt'],
                    rnk = baby['rnk'])
    session.add(new_baby)

for doggo in doggos:
    if 'animalgender' not in doggo:
        doggo['animalgender'] = 'None Specified'
    new_doggo = Doggo(rownumber = int(doggo['rownumber']),
                     animalname = doggo['animalname'],
                     animalgender = doggo['animalgender'],
                     animalbirth = int(doggo['animalbirth']),
                     breedname = doggo['breedname'],
                     zipcode = doggo['zipcode'],
                     licenseissueddate = doggo['licenseissueddate'],
                     licenseexpireddate = doggo['licenseexpireddate'],
                     extract_year = int(doggo['extract_year']))
    session.add(new_doggo)

session.commit()
session.close()