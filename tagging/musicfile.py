# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
from mutagen.id3._util import ID3NoHeaderError
from mutagen.mp3 import MP3, HeaderNotFoundError
EasyMP4.RegisterTextKey('airplayid', 'apID')
from os.path import join, splitext, basename
import re

class MusicFile(object):
    """
    Base class for music files.
    """

    taggers = {
        '.mp3': EasyID3,
        '.m4a': EasyMP4,
        '.m4p': EasyMP4
    }

    def __init__(self, root, filename):
        """
        Initialize the file object.
        :param filename:
        :return:
        """

        self.root = root
        self.filename = filename
        self.filetype = splitext(filename)[1][1:]
        self.tags = None

    def __str__(self):
        s = self.filename
        if self.tags:
            s = s + u" --> artist:{} album:{} title:{}".format(
                self.artist,
                self.album,
                self.title
            )
        return s

    @property
    def name(self):
        return self.filename

    @property
    def base_filename(self):
        if self.filename.startswith('./'):
            return self.filename[2:]
        return self.filename

    @property
    def artist(self):
        """
        Return artist name, or Unknown
        :return:
        """
        return self.tags.get('artist', ['Unknown'])[0]

    @property
    def album(self):
        """
        Return album name, or Unknown
        :return:
        """
        return self.tags.get('album', ['Unknown'])[0]

    @property
    def title(self):
        """
        Get the title from the tags, or use the filename as the title if not found.
        :return:
        """
        return self.tags.get('title', splitext(basename(self.filename)))[0]

    @property
    def type(self):
        return self.filetype.lower()

    def clean_strings(self, s):
        """
        Remote characters from strings that can't be used in a path or filename.
        :param s:
        :return:
        """
        return re.sub(r'[^\w\d .-_]', '', s)

    def calc_ideal_path(self):
        """
        This function will calculate the ideal path for this file.

        Modify this in order to change how we organize the files... for now its using this:

        artist/album/<title>.<filetype>


        :return:
        """
        filename = "{}/{}/{}.{}".format(
            self.clean_strings(self.artist),
            self.clean_strings(self.album),
            self.clean_strings(self.title),
            self.type
        )
        return filename

    def tag(self, show=False):
        """
        Tag the current file
        :return:
        """

        fullfile = join(self.root,self.filename)
        ext = splitext(self.filename)[1]

        try:
            tagger = self.taggers.get(ext)
            if tagger:
                tags = tagger(fullfile)
                self.tags = {k: tags.get(k) for k in tags.keys()}
                show and self.showtags(self.tags)
        except HeaderNotFoundError:
            print("Did not parse:{}".format(fullfile))
        except ID3NoHeaderError:
            print("Did not parse:{}".format(fullfile))
        except Exception as e:
            print("Some unknown reason we failed: {}.".format(e))

    def showtags(self, tags):
        """
        Display the tags from the tag field.
        :param tags:
        :return:
        """
        for k in tags.keys():
            print(u"{}:{}".format(
                k, tags.get(k)[0]
            ))
        print('\n')

