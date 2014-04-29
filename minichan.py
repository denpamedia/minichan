from bottle import route, request, run, template, static_file, post, redirect, Bottle
from datetime import datetime
from time import time
from model import *
from config import *

app = Bottle()

########################################################################################################################
# Import CSS and JS

@app.route('/static/css/bootstrap.min.css')
def callback0():
    return static_file('bootstrap.min.css', root='static/css')

@app.route('/static/css/mystyle.css')
def callback1():
    return static_file('mystyle.css', root='static/css')

@app.route('/static/js/jquery.js')
def callback2():
    return static_file('jquery.js', root='static/js')

@app.route('/static/js/bootstrap.min.js')
def callback3():
    return static_file('bootstrap.min.js', root='static/js')

########################################################################################################################
# Redirecting

@app.route('/')
def wrong0():
    redirect('/b')

@app.route('/<board>/')
def wrong1(board):
	redirect('/' + board)

@app.route('/<board>/<thread>/')
def wrong2(board, thread):
	redirect ('/' + board + '/' + thread)

########################################################################################################################
# Controllers

# Show a list of board threads
@app.route('/<board>')
def get_threads(board):
	# Get list of board threads
	with switch_db(Thread, board) as myThread:
		thread_list = (one_thread for one_thread in myThread.objects)
	return template('static/board.tpl', board_list=board_list, board=board, thread_list=thread_list)

# Make a new thread on board
@app.post('/<board>')
def new_thread(board):
	# Use POST method to get data
	subject = request.forms.getunicode('subject')
	body = request.forms.getunicode('body')
	# Update post counter
	with switch_db(Counter, board) as myCounter:
		post_id = [counter.last_id for counter in myCounter.objects(name='post_counter')][0] + 1
		myCounter.objects(name='post_counter').update_one(inc__last_id=1)
	# Make new thread on board
	with switch_db(Thread, board) as myThread:
		myThread(subject=subject, body=body, creation_time=datetime.now().strftime("%d.%m.%Y %H:%M:%S"), post_id=post_id , bump_time=time()).save()
	# Redirect to the board page
	redirect('/' + board)

# Show a list of thread replies
@app.route('/<board>/<thread>')
def get_replies(board, thread):
	# Get original post of thread
	with switch_db(Thread, board) as myThread:
		mythread=[one_thread for one_thread in myThread.objects(post_id=thread)][0]
	# Get list of thread replies
	with switch_db(Reply, board) as myReply:
		reply_list=(reply for reply in myReply.objects(op_link=thread))
	return template('static/thread.tpl', board_list=board_list, board=board, thread_number=thread, thread=mythread, reply_list=reply_list)

# Make a new reply
@app.post('/<board>/<thread>')
def new_reply(board, thread):
	# Use POST method to get data
	subject = request.forms.getunicode('subject')
	body = request.forms.getunicode('body')
	# Update post counter
	with switch_db(Counter, board) as myCounter:
		post_id = [counter.last_id for counter in myCounter.objects(name='post_counter')][0] + 1
		myCounter.objects(name='post_counter').update_one(inc__last_id=1)
	# Update last bump and bump counter of thread
	with switch_db(Thread, board) as myThread:
		myThread.objects(post_id=thread).update_one(inc__bump_counter=1)
		myThread.objects(post_id=thread).update_one(set__bump_time=time())
	# Make new reply on thread
	with switch_db(Reply, board) as myReply:
		Reply(subject=subject, body=body, creation_time=datetime.now().strftime("%d.%m.%Y %H:%M:%S"), post_id=post_id, op_link=thread).save()
	redirect ('/' + board + '/' + thread)

########################################################################################################################
# Run

run(app, host='localhost', port=8080)

