# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import time

class TimeTrack:

    def __init__(self, start_msg="Starting."):
        self.msg = start_msg

    def __enter__(self):
        print(self.msg)
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        print('Done in {}'.format(self.interval))

