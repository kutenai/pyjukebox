__author__ = 'kutenai'

from flask import Flask
app = Flask(__name__)
import pyglet

@app.route('/')
def hello_world():

    song = pyglet.media.load('thesong.ogg')
    song.play()
    pyglet.app.run()
    return "Hello, World"


if __name__ == '__main__':
    app.run()


