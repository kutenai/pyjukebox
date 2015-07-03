# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql+psycopg2://postgres:iD9aD5tIv7Jov0@localhost:5433/archive_production_mirror")
metadata = MetaData(engine)
Base = declarative_base()

class Songs(Base):
    __table__ = Table('songs', metadata, autoload=True)

