from flask import request, redirect, render_template, make_response
from app import minichan
from app import controller
from app import model


@minichan.route('/', methods=['GET', 'POST'])
def board():
    if request.method == 'POST':
        controller.make_new_thread(body=request.form['body'],
            subject=request.form['subject'],
            image=request.files['image'])
        return redirect('/')
    else:
        return render_template('board.html', data=model.Thread.all)


@minichan.route('/<int:thread_id>', methods=['GET', 'POST'])
def thread(thread_id):
    if request.method == 'POST':
        body = request.form['body']
        image = request.files['image']
        controller.make_new_reply(thread_id=thread_id, body=body, image=image)
        return redirect('/{0}'.format(thread_id))
    else:
        data = controller.get_thread(thread_id)
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

