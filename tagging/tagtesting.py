# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'kutenai'


from os.path import exists
import argparse

from visitor import Visitor

#root = '/Users/kutenai/proj/bondiproj/pyjukebox/MajorTunage'

music_extensions = ['.mp3', '.m4a']


def showid(type, id):
    print("Type{}".format(type))
    for k in id.keys():
        print(u"{}:{}".format(
            k, id.get(k)[0]
        ))
    print('\n')

def main():

    parser = argparse.ArgumentParser(description='Tag Music Files.')
    parser.add_argument('root',
                        help='Root path for files to tag.')

    parser.add_argument('--freezefile',
                        help='Freeze the data from the initial read to this file.')

    parser.add_argument('--extensions', nargs='+',
                        default=['mp3', 'm4a', 'm4p'],
                        help="List of extensions to search for.")

    parser.add_argument('--logfile',
                        help='Log for tag logging data.')

    args = parser.parse_args()

    visitor = Visitor(args.extensions)

    if args.freezefile and exists(args.freezefile):
        visitor.thaw(args.freezefile)
    else:
        visitor.find_files(args.root)

        print("Found a total of {} {} files.".format(visitor.count, visitor.type))

        if args.logfile:
            with open(args.logfile, 'w') as fp:
                visitor.tagall(logfp=fp)
        else:
            visitor.tagall()

        if args.freezefile:
            visitor.freeze(args.freeze)



if __name__ == "__main__":

    main()