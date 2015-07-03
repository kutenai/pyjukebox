__author__ = 'kutenai'

from collections import defaultdict
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
from mutagen.id3._util import ID3NoHeaderError
from mutagen.mp3 import MP3, HeaderNotFoundError
EasyMP4.RegisterTextKey('airplayid', 'apID')
from os.path import walk, join, splitext, relpath, exists
import pickle

from musicfile import MusicFile

class Visitor(object):
    """
    Used in the visit function when iterating over directories.
    Class will find files of it's particular type, and store them
    into a list for later use.
    """

    def __init__(self, extensions):
        """
        Initialize the class with the extension this class will look for and handle.
        :param extension:
        :return:
        """
        self.extensions = []
        for extension in extensions:
            if not extension.startswith('.'):
                extension = '.' + extension
            self.extensions.append(extension.lower())

        self.data = {
            'root': None,
            'byorder': [],
            'bytype': defaultdict(list),
            'byname': {}
        }

    @property
    def count(self):
        return len(self.data['byorder'])

    @property
    def type(self):
        return ",".join(self.extensions)

    @property
    def root(self):
        return self.data.get('root', None)

    @property
    def byorder(self):
        return self.data.get('byorder', [])

    def is_my_files(self, f):
        """
        Filter out files that don't match my extension.

        The special ._ prefix is some sort of 'system' file that we want to
        ignore all of the time.

        :param f:
        :return:
        """
        if f.startswith('._'):
            return False

        return splitext(f)[1].lower() in self.extensions

    def visit(self, root, dirname, names):
        """
        Check the names and see if any match the extension we are
        configured to look for. Save the matching files to our list.
        """

        myfiles = filter(self.is_my_files, names)
        byname = self.data['byname']
        bytype = self.data['bytype']

        if len(myfiles):
            base = relpath(dirname, root)
            music_files = [MusicFile(root, join(base, f)) for f in myfiles]
            self.data['byorder'].extend(music_files)
            for mf in music_files:
                byname[mf.name] = mf
                bytype[mf.type].append(mf)
            #print("Added {} files.".format(len(myfiles)))


    def find_files(self, root):
        """
        Visit all files in the root path.
        For each file found, let the visitors process
        the file list and store the files that match
        their file type.

        Store the root path as a class variable for all visitors
        to use later.
        """

        self.data['root'] = root

        walk(root, self.visit, root)

    def tagall(self, logfp=None):
        """
        Do some tagging, depending on the type of files.
        :return:
        """
        allfiles = self.data['byorder']

        num_to_tag = len(allfiles)
        num_tagged = 0
        for file in allfiles:
            file.tag()
            num_tagged += 1
            if not num_tagged% 100:
                print("Tagged {} of {}".format(num_tagged, num_to_tag))

    def freeze(self, freezefile):
        """
        Save a freeze file for all data for this type of file.
        :param path:
        :return:
        """
        with open(freezefile, 'wb') as fp:
            pickle.dump(self.data, fp)

    def thaw(self, freezefile):
        """
        Restore from the pickle file
        :param path:
        :return:
        """

        if exists(freezefile):
            with open(freezefile, 'rb') as fp:
                self.data = pickle.load(fp)


