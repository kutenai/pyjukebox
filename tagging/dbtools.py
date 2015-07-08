# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base

from os.path import relpath, join
def main():

    engine = create_engine("postgresql+psycopg2://postgres:iD9aD5tIv7Jov0@localhost:5433/archive_production_mirror")
    metadata = MetaData(engine)
    Base = declarative_base()

    Session = sessionmaker(bind=engine)
    session = Session()
    basepath = '/Volumes/MajorTuneage'
    filename = '/Volumes/MajorTuneage/disk0/mp3/Tapia/07 Mentirosos.m4a'
    filename2 = '/This is a bogus file'

    class Songs(Base):
        __table__ = Table('songs', metadata, autoload=True)

        @classmethod
        def update_file(cls, old_file, new_file):
            s = session.query(Songs).filter_by(file=old_file).one()
            print("Found song:{}".format(s.id))
            s.file = new_file
            session.commit()
            print("Updated song")

    allfiles = session.query(Songs).all()
    filehash = set()

    with Timer('Updating filenames.') as t:
        for f in allfiles:
            filehash.add(f.file)
            if f.file.startswith(basepath):
                newf = relpath(f.file, basepath)
                if newf != f.file:
                    f.file = newf
            else:
                f.file = join(basepath,f.file)

    with Timer('Commit changes') as t:
        session.commit()


if __name__ == "__main__":
    main()