# -*- coding: utf-8 -*-

import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash


# configuration
DATABASE = '/tmp/radio_dashboard.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where id = ?',
                          [session['user_id']], one=True)


@app.route('/')
def index():
    return redirect(url_for('broadcasts', page=1))


class Announcement:
    @staticmethod
    def get_all():
        sql = 'select * from announcement'
        return query_db(sql)


    @staticmethod
    def add_new(text=''):
        db = get_db()
        db.execute('insert into announcement (text) values (?)',
                  [text])
        db.commit()

def test_data():
    return [
            {

                'from_time': '2015-10-15T19:21:13+03:00',
                'to_time': '',
                'cover_url': 'images/1444497910945.jpg',
                'txt': u'''
<p>Сегодня в 20:30 на +Радио 410 начнётся небольшой эфир, посвящённый психоделик-року, ololo.</p>
<p>Вы сможете услышать краткий неполный обзор дискографий американских команд Dengue Fever (LA) и Snail (Сиэтл), кроме того прозвучит небольшая подборка из продукции лейбла Riding Easy Records, который базируется в тихом пляжном городке Эрмоса-бич штат Калифорния.</p>
<p> Не надо открывать поток браузером! Если вы не знаете, что с ним делать, откройте плейлист.  </p>
<p> Поток: <a href="http://radio.410chan.ru:8000/radio">http://radio.410chan.ru:8000/radio</a> </p>
<p> Плейлист: <a href="http://radio.410chan.ru:8000/radio.m3u">http://radio.410chan.ru:8000/radio.m3u</a> </p>'''
            },
            {

                'from_time': '2015-10-15T18:21:13+03:00',
                'to_time': '',
                'cover_url': 'images/1444497910945.jpg',
                'txt': u'''
<p>Сегодня в 20:30 на +Радио 410 начнётся небольшой эфир, посвящённый психоделик-року, ololo.</p>
<p>Вы сможете услышать краткий неполный обзор дискографий американских команд Dengue Fever (LA) и Snail (Сиэтл), кроме того прозвучит небольшая подборка из продукции лейбла Riding Easy Records, который базируется в тихом пляжном городке Эрмоса-бич штат Калифорния.</p>
<p> Не надо открывать поток браузером! Если вы не знаете, что с ним делать, откройте плейлист.  </p>
<p> Поток: <a href="http://radio.410chan.ru:8000/radio">http://radio.410chan.ru:8000/radio</a> </p>
<p> Плейлист: <a href="http://radio.410chan.ru:8000/radio.m3u">http://radio.410chan.ru:8000/radio.m3u</a> </p>'''
            },
            {

                'from_time': '2015-10-15T19:21:13+03:00',
                'to_time': '',
                'cover_url': 'images/1444497910945.jpg',
                'txt': u'''
<p>Сегодня в 20:30 на +Радио 410 начнётся небольшой эфир, посвящённый психоделик-року, ololo.</p>
<p>Вы сможете услышать краткий неполный обзор дискографий американских команд Dengue Fever (LA) и Snail (Сиэтл), кроме того прозвучит небольшая подборка из продукции лейбла Riding Easy Records, который базируется в тихом пляжном городке Эрмоса-бич штат Калифорния.</p>
<p> Не надо открывать поток браузером! Если вы не знаете, что с ним делать, откройте плейлист.  </p>
<p> Поток: <a href="http://radio.410chan.ru:8000/radio">http://radio.410chan.ru:8000/radio</a> </p>
<p> Плейлист: <a href="http://radio.410chan.ru:8000/radio.m3u">http://radio.410chan.ru:8000/radio.m3u</a> </p>'''
            },
            {

                'from_time': '2015-10-15T19:21:13+03:00',
                'to_time': '',
                'cover_url': 'images/1444497910945.jpg',
                'txt': u'''
<p>Сегодня в 20:30 на +Радио 410 начнётся небольшой эфир, посвящённый психоделик-року, ololo.</p>
<p>Вы сможете услышать краткий неполный обзор дискографий американских команд Dengue Fever (LA) и Snail (Сиэтл), кроме того прозвучит небольшая подборка из продукции лейбла Riding Easy Records, который базируется в тихом пляжном городке Эрмоса-бич штат Калифорния.</p>
<p> Не надо открывать поток браузером! Если вы не знаете, что с ним делать, откройте плейлист.  </p>
<p> Поток: <a href="http://radio.410chan.ru:8000/radio">http://radio.410chan.ru:8000/radio</a> </p>
<p> Плейлист: <a href="http://radio.410chan.ru:8000/radio.m3u">http://radio.410chan.ru:8000/radio.m3u</a> </p>'''
            },
            {
                'from_time': '2015-10-15T19:21:13+03:00',
                'to_time': '',
                'cover_url': 'images/2.jpg',
                'txt': u'''
<p>Добрый вечер!</p>
<p>Сегодня в 20:00 московского времени на Радио 410 начнётся спонтанный субботне-вечерний эфир без чёткой жанровой направленности.</p>
<p>Брант Бьорк, Ноэль Галлахер, слегка протухший ретровейв, польский психоделик, немного японщины, джаз и, конечно, ваши реквесты будут звучать сегодня на Радио 410 с одной единственной целью: попробовать создать атмосферу спокойного субботнего вечера в условиях стремительно приближающегося лета.</p>
<p>OGG: http://radio.410chan.ru:8000/live.ogg MP3: http://libera.thordendal.ru:8000/radio.mp3</p>
<p>Jabber: thordendal@thordendal.ru</p>
<p>Реквесты можно заливать на любой удобный вам файлообменник.</p>'''
            }
            ]


@app.route('/broadcasts/<page>')
def broadcasts(page):
    #broadcasts = Announcement.get_all()
    broadcasts = test_data()
    return render_template('index.html', broadcasts=broadcasts)
#    sql = 'select count(*) as cnt from announcement'
#    broadcasts_cnt = query_db(sql, one=True)


    return render_template('broadcasts.html', broadcasts=broadcasts)


@app.route('/broadcasts/new', methods=['POST'])
def broadcasts_new():
    # TODO: check access
    text = request.form['message']
    Announcement.add_new(text=text)
    return redirect(url_for('index'))
    #return render_template('broadcasts.html', broadcasts=broadcasts)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
