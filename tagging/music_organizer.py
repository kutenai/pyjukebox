# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from os.path import join, dirname
from shutil import copy
from distutils.dir_util import mkpath

from archivedb import engine, Songs

### another way (but again *not the only way*) to do it ###

from contextlib import contextmanager

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        print("Committing all changes..")
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class MusicOrganizer(object):
    """
    Organize music files by title, artist, album, etc.
    Update the pgsql database file path to match the new path.

    Takes a Visitor object as a constructor parameter. This Visitor
    will be used to get the list of MusicFile objects, their tags, and
    their other information.
    """

    def __init__(self, visitor=None):

        self.visitor = visitor
        self.basepath = '/Volumes/MajorTuneage'

    def organize_all(self, srcroot, destroot):
        """
        Update the files to their new calculated location.
        If their new location differs from their old location, then copy
        the file to the new location, and update the database.
        :return:
        """
        total_files = len(self.visitor.byorder)
        counter = 0

        with session_scope() as session:

            for file in self.visitor.byorder:
                newpath = file.calc_ideal_path()
                if not file.base_filename.startswith('/'):
                    dest_path = join(destroot, newpath)

                    original_path = join('/Volumes/MajorTuneage', file.base_filename)
                    src_path = join(srcroot, file.base_filename)
                    try:
                        song = session.query(Songs).filter_by(file=original_path).first()
                        if song:
                            song.file = newpath
                            mkpath(dirname(dest_path))
                            copy(src_path, dest_path)
                    except NoResultFound as e:
                        print("Song {} does not exist in database.".format(file.base_filename))
                    except Exception as e:
                        print("Failed to copy the song:{} Exception:{}".format(file.base_filename, e))

                counter += 1
                if not counter % 100:
                    print("Re-organized {} of {} files.".format(counter, total_files))








