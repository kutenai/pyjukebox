# -*- coding: utf-8 -*-
__author__ = 'kutenai'


import os
from os.path import join, splitext
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.mp4 import MP4, MP4Tags
from mutagen.easymp4 import EasyMP4
EasyMP4.RegisterTextKey('airplayid', 'apID')


root = '/Volumes/Tuneage/MajorTuneage'
music_extensions = ['.mp3', '.m4a']

mp3_files = []
aac_files = []
def is_music_file(f):
    return os.path.splitext(f)[1] in music_extensions

def is_mp3_file(f):
    if f.startswith('._'):
        return False
    return os.path.splitext(f)[1] in ['.mp3']

def is_aac_file(f):
    if f.startswith('._'):
        return False

    return os.path.splitext(f)[1] in ['.m4a']

def visit_dirs(arg, dirname, names):
    mp3 = filter(is_mp3_file, names)
    aac = filter(is_aac_file, names)

    if len(mp3):
        base = os.path.relpath(dirname, root)
        music_files = [os.path.join(base, f) for f in mp3]
        mp3_files.extend(music_files)

    if len(aac):
        base = os.path.relpath(dirname, root)
        music_files = [os.path.join(base, f) for f in aac]
        aac_files.extend(music_files)

    #print("Found {} mp3 files in {}".format(len(mp3), dirname))
    #print("Found {} aac files in {}".format(len(aac), dirname))



def find_files(root):
    """
    Find files recursively on the given path.
    :param dir:
    :return:
    """

    os.path.walk(root, visit_dirs, {})
    return mp3_files, aac_files

def showid(type, id):
    print("Type{}".format(type))
    for k in id.keys():
        print(u"{}:{}".format(
            k, id.get(k)[0]
        ))
    print('\n')

def main():
    mp3_files, aac_files = find_files(root)
    print("Found a total of {} mp3 files".format(len(mp3_files)))
    print("Found a total of {} aac files".format(len(aac_files)))

    for file in mp3_files:
        file = join(root,file)
        try:
            audio = MP3(file)
            id = ID3(file)
            eid = EasyID3(file)
            showid('MP3', eid)
        except HeaderNotFoundError:
            print("Did not parse:{}".format(file))
        except ID3NoHeaderError:
            print("Did not parse:{}".format(file))

    for file in aac_files:
        file = join(root,file)
        audio = MP4(file)
        #id = ID3(join(root,file))
        eid = EasyMP4(file)
        showid('AAC', eid)
        pass

if __name__ == "__main__":

    main()