__author__ = 'kutenai'

import pyglet
from time import sleep


class JukePlayer(object):
    """
    Base class for the player.
    This will wrap the pyglet player code, and
    provide the high level interface for playing
    songs.
    """

    def __init__(self):
        self.p1 = pyglet.media.Player()
        self.p2 = pyglet.media.Player()
        self._curr = self.p1

    def _next_player(self):
        """Get the next player to use"""
        if self.p1 == self._curr:
            return self.p2
        return self.p1

    def crossfade(self,p1, p2, seconds=3.0):
        """
        Crossfade p2 then p2
        :param p1:
        :param p2:
        :return:
        """

        sref=int(seconds*10)

        for a in range(0, sref):
            v2 = float(a)/float(sref)
            v1 = 1.0-v2
            p1.volume = v1
            p2.volume = v2

            sleep(0.1)

        p2.volume = 1.0
        p1.volume = 0

    def play(self, file):
        """
        Get the next available player.
        If there is a song currently playing, then
        crossfade the current song with it.
        file.
        :param file:
        :return:
        """

        source = pyglet.media.load(file)
        player = self._next_player()
        player.queue(source)
        if self._curr.playing:
            player.volume = 0
            player.play()
            self.crossfade(self._curr, player)
        else:
            player.volume = 1
            player.play()

        self._curr = player

    @property
    def time(self):
        """Get time of currently playing song"""
        return self._curr.time

