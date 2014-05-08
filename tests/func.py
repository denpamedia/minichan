import minichan
from webtest import TestApp

def test_thread_index():
    app = TestApp(minichan.app)
    assert app.get('/b').status == '200 OK'

def test_create_thread():
	app = TestApp(minichan.app)
	app.post('/b',{'subject':'test','body':'hi there'}).status == '304 Found'