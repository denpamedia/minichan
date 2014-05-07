from bottle import redirect, template, static_file, request, abort

from app import app
from app.controller import *
from app.config import *

#Generation of assets
from webassets import Environment
from webassets import Bundle

env = Environment('app/static/',url='/static/')
js = Bundle('js/jquery.js','js/bootstrap.js', output='gen/packed.js')
env.register('js_all', js)

css = Bundle('css/mystyle.css','css/bootstrap.min.css', output='gen/packed.css')
env.register('css_all', css)


# Route for Original Posts list.
@app.route('/<board>')
def show_board(board):
    '''Return board.tpl template and Original Posts data,
    using get_original_posts_iter function from controller module.

    If there are not such Board, return 404 Page.

    '''
	
    try:
        original_posts_iter = get_original_posts_iter(board=board)

        return template('app/static/board.tpl', board=board, bump_limit=BUMP_LIMIT,
            board_list=BOARD_LIST, original_posts_iter=original_posts_iter,
            js_assets=env['js_all'].urls()[0],
            css_assets=env['css_all'].urls()[0])
    except:
        return abort(404, 'This page does not exist')


# Route for Reply Posts list.
@app.route('/<board>/<thread>')
def show_thread(board, thread):
    '''Return thread.tpl template and also Original Post and it's Reply Posts data,
    using get_original_post and get_reply_posts_iter functions from controller module.

    If there are not such Board or Original Post or Reply Posts, return 404 Page.

    '''

    try:
        original_post = get_original_post(board=board, original_post_id=thread)
        reply_posts_iter = get_reply_posts_iter(board=board, original_post_id=thread)

        return template('app/static/thread.tpl', thread=thread, board=board, bump_limit=BUMP_LIMIT,
            board_list=config.BOARD_LIST, original_post=original_post, reply_posts_iter=reply_posts_iter,
            js_assets=env['js_all'].urls()[0],
            css_assets=env['css_all'].urls()[0]
        )
    except:
        return abort(404, 'This page does not exist')


# Route for make new Original Post. Use POST method.
@app.post('/<board>')
def make_thread(board):
    '''Get posting form data.
    Then use set_original_post function from controller module to make new Original Post.

    '''
	
    subject = request.forms.getunicode('subject')
    body = request.forms.getunicode('body')

    set_original_post(board=board, subject=subject, body=body)

    redirect('/' + board)


# Route for make new Reply Post. Use POST method.
@app.post('/<board>/<thread>')

def make_reply(board, thread):
    '''Get posting form data.
    Then use set_reply_post function from controller module to make new Reply Post.	

    '''

    subject = request.forms.getunicode('subject')
    body = request.forms.getunicode('body')

    set_reply_post(board=board, original_post_id=thread, subject=subject, body=body)

    redirect('/' + board + '/' + thread)



# Redirect from '/' Page to 'b' Board
@app.route('/')
def goto_b():
    redirect('/b')



# Routes for CSS and JavaScript static files
@app.route('/static/gen/packed.css')
def callback2():
    return static_file('packed.css', root='app/static/gen')


@app.route('/static/gen/packed.js')
def callback2():
    return static_file('packed.js', root='app/static/gen')