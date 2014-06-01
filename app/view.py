from time import time
from datetime import datetime
import hashlib

from flask import request, redirect, render_template, make_response

from app import minichan
from app import model
from app import config


@minichan.route('/', methods=['GET', 'POST'])
def board():
    if request.method == 'POST':
        if model.Thread.objects.count() >= config.NUMBER_OF_THREADS:
            model.Thread.oldest.delete()

        thread = model.Thread()
        thread.post_id = next_counter()
        thread.body = request.form['body']
        thread.subject = request.form['subject']
        thread.bump_time = time()
        thread.creation_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        thread.save()

        try:
            image = model.Image(post_link=thread)
            image.img_src.put(request.files['file'])
            image.img_id = str(hashlib.md5(image.img_src.read()).hexdigest())
            image.save()
            thread.update(set__image_id=image.img_id)
        except:
            pass

        return redirect('/')
    else:
        return render_template('board.html', data=model.Thread.all)


@minichan.route('/<thread_id>', methods=['GET', 'POST'])
def thread(thread_id):
    if request.method == 'POST':
        original_post = model.Thread.objects(post_id=thread_id)[0]
        original_post.update(inc__bump_counter=1)
        if original_post.bump_counter >= config.BUMP_LIMIT:
            original_post.update(set__bump_limit=True)
        else:
            original_post.update(set__bump_time=time())

        reply = model.Reply()
        reply.post_id = next_counter()
        reply.creation_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        reply.body = request.form['body']
        reply.thread_link = original_post
        reply.save()

        try:
            image = model.Image(post_link=reply)
            image.img_src.put(request.files['file'])
            image.img_id = str(hashlib.md5(image.img_src.read()).hexdigest())
            image.save()
            reply.update(set__image_id=image.img_id)
        except:
            pass

        return redirect('/{0}'.format(thread_id))
    else:
        data = {
        "original_post": dict(model.Thread.objects(post_id=thread_id)[0].to_mongo()),
        "reply_list": [dict(reply.to_mongo()) for reply in model.Reply.all(thread_link=model.Thread.objects(post_id=thread_id)[0])]
        }
        return render_template('thread.html', data=data)
        


@minichan.route('/<img_type>/<img_id>', methods=['GET'])
def image(img_type, img_id):
    if img_type == 'thumb':
        image = model.Image.objects(img_id=img_id)[0]
        myimage = image.img_src.thumbnail.read()
        response = make_response(myimage)
        response.headers['Content-Type'] = 'image/jpeg'
        return response
    else:
        image = model.Image.objects(img_id=img_id)[0]
        myimage = image.img_src.read()
        response = make_response(myimage)
        response.headers['Content-Type'] = 'image/jpeg'
        return response


def next_counter():
    model.Counter.objects(name='post_counter').update_one(inc__next_id=1)
    return model.Counter.objects[0].next_id