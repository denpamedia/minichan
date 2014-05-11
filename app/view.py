import json

from bottle import redirect, template, static_file, request, abort

from webassets import Environment
from webassets import Bundle

from app import app
from app.controller import *
from app.config import *


env = Environment('app/static/',url='/static/')
js = Bundle('js/jquery.js','js/bootstrap.js', output='gen/packed.js')
env.register('js_all', js)

css = Bundle('css/mystyle.css','css/bootstrap.min.css', output='gen/packed.css')
env.register('css_all', css)


@app.route('/<board>')
@app.route('/<board>/')
def show_board(board):
    board_json = get_board(board=board)

    return template('app/static/board.tpl', board_json=board_json,
        js_assets=env['js_all'].urls()[0], css_assets=env['css_all'].urls()[0])


@app.route('/<board>/<thread>')
@app.route('/<board>/<thread>/')
def show_thread(board, thread):
    thread_json = get_thread(board=board, thread=thread)
    
    return template('app/static/thread.tpl', thread_json=thread_json,
        js_assets=env['js_all'].urls()[0], css_assets=env['css_all'].urls()[0])




@app.post('/<board>')
@app.post('/<board>/')
def make_thread(board):
    subject = request.forms.getunicode('subject')
    body = request.forms.getunicode('body')

    set_thread(board=board, subject=subject, body=body)

    redirect('/' + board)


@app.post('/<board>/<thread>')
@app.post('/<board>/<thread>/')
def make_reply(board, thread):
    subject = request.forms.getunicode('subject')
    body = request.forms.getunicode('body')

    set_reply(board=board, thread=thread, subject=subject, body=body)

    redirect('/' + board + '/' + thread)




# Routes for CSS and JavaScript static files
@app.route('/static/gen/packed.css')
def callback():
    return static_file('packed.css', root='app/static/gen')


@app.route('/static/gen/packed.js')
def callback2():
    return static_file('packed.js', root='app/static/gen')