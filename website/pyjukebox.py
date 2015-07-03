__author__ = 'kutenai'

import sqlite3
from flask import Flask, render_template, url_for, request
from time import sleep
from player.player import JukePlayer
from contextlib import closing

# configuration
DATABASE = 'jukebox.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
#app.config.from_envvar('JUKEBOX_SETTINGS', silent=True)
app.config.from_object(__name__)

player = JukePlayer()

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def hello_world():
    return render_template('index.html',
                           song1=url_for('play_song', songid=1),
                           song2=url_for('play_song', songid=2))

@app.route('/play/<int:songid>')
def play_song(songid):


    if songid == 1:
        file='/Users/kutenai/proj/bondiproj/pyjukebox/MajorTunage/disk0/mp3/0Singles/Alabama/Alabama - Five O\'Clock 500.mp3'
    else:
        file='/Users/kutenai/proj/bondiproj/pyjukebox/MajorTunage/disk0/mp3/0Singles/Ben Folds Five/Battle of Who Could Care Less.mp3'

    player.play(file)

    return ""

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()


