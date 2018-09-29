# how to create a Django-Project?
[python3 tutorial](https://docs.python.org/3/tutorial/)
[flask](http://flask.pocoo.org)
<br>
[flask quickstart](http://flask.pocoo.org/docs/1.0/quickstart)
[flask tutorial](http://flask.pocoo.org/docs/1.0/tutorial/)


## Install
Create a project folder and a venv folder within:

python2.7
```bash
virtualenv venv
```

python3
```bash
mkdir myproject
cd myproject
python3 -m venv venv
```

Activate the environment:
```bash
. venv/bin/activate
```

```bash
pip install Flask
```


## Run Server
```bash
# The FLASK_APP environment variable is the name of the module to import at flask run.
export FLASK_APP=hello.py

# To enable all development features (including debug mode) you can export the FLASK_ENV environment variable and set it to development before running the server:
# You can also control debug mode separately from the environment by exporting FLASK_DEBUG=1.
# FLASK_DEBUG number:
# 1. it activates the debugger
# 2. it activates the automatic reloader
# 3. it enables the debug mode on the Flask application.
# must never be used on production machines.
export FLASK_ENV=development

# with configable host and port
flask run --host=0.0.0.0 --port=8889
```

This launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production. For deployment options see [Deployment Options](http://flask.pocoo.org/docs/1.0/deploying/#deployment).


## Routing
Modern web applications use meaningful URLs to help users. Users are more likely to like a page and come back if the page uses a meaningful URL they can remember and use to directly visit a page.

Use the `route()` decorator to bind a function to a URL.

```python
@app.route('/')
def index():
  return 'Index Page'

@app.route('/hello')
def hello():
  return 'Hello, World'
```

You can do more! You can make parts of the URL dynamic and attach multiple rules to a function.

### Variable Rules
You can add variable sections to a URL by marking sections with ``<variable_name>``. Your function then receives the ``<variable_name>`` as a keyword argument. Optionally, you can use a converter to specify the type of the argument like ``<converter:variable_name>``.

```python
@app.route('/user/<username>')
def show_user_profile(username):
  # show the user profile for that user
  return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
  # show the post with the given id, the id is an integer
  return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
  # show the subpath after /path/
  return 'Subpath %s' % subpath
```
Converter types:
|type|desc|
|:----:|:---|
|string| accepts any text without a slash |
|int|	accepts positive integers |
|float |	accepts positive floating point values |
|path |	like string but also accepts slashes |
|uuid |	accepts UUID strings |


### URL Building
To build a URL to a specific function, use the `url_for()` function. It accepts the name of the function as its first argument and any number of keyword arguments, each corresponding to a variable part of the URL rule. Unknown variable parts are appended to the URL as query parameters.

1. Reversing is often more descriptive than hard-coding the URLs.
2. You can change your URLs in one go instead of needing to remember to
manually change hard-coded URLs.
3. URL building handles escaping of special characters and Unicode data
transparently.
4. The generated paths are always absolute, avoiding unexpected behavior of relative paths in browsers.
5. If your application is placed outside the URL root, for example, in
`/myApplication` instead of `/`, `url_for()` properly handles that for you.

```python
from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def index():
  return 'index'

@app.route('/login')
def login():
  return 'login'

@app.route('/user/<username>')
def profile(username):
  return '{}\'s profile'.format(username)

with app.test_request_context():
  print(url_for('index'))
  print(url_for('login'))
  print(url_for('login', next='/'))
  print(url_for('profile', username='John Doe'))
```

it outputs:
```
/
/login
/login?next=%2F
/profile?username=John+Doe
```

### HTTP Methods
```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    return do_the_login()
  else:
    return show_the_login_form()
```

If GET is present, Flask automatically adds support for the `HEAD` method and handles `HEAD` requests according to the [HTTP RFC](https://www.ietf.org/rfc/rfc2068.txt). Likewise, `OPTIONS` is automatically implemented for you.


### Static Files
To generate URLs for static files, use the special 'static' endpoint name:

```python
url_for('static', filename='style.css')
```
The file has to be stored on the filesystem as `static/style.css`.


### Rendering Templates
Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the `HTML` escaping on your own to keep the application secure. Because of that Flask configures the `Jinja2` template engine for you automatically.

To render a template you can use the ``render_template()`` method. All you have to do is provide the name of the template and the variables you want to pass to the template engine as keyword arguments. Here’s a simple example of how to render a template:

```python
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('hello.html', name=name)
```

Flask will look for templates in the `templates` folder. So if your application is a module, this folder is next to that module, if it’s a package it’s actually inside your package:

+ Case 1: a module:
```
/application.py
/templates
  - hello.html
```

+ Case 2: a package:
```
/application
  /__init__.py
  /templates
    - hello.html
```

### Jinja2 templates
Head over to the official [Jinja2](http://jinja.pocoo.org/docs/2.10/templates/) Template Documentation for more information.

Inside templates you also have access to the `request`, `session` and `g` objects as well as the `get_flashed_messages()` function.

If you can trust a variable and you know that it will be safe HTML (for example because it came from a module that converts wiki markup to HTML) you can mark it as safe by using the [Markup](http://jinja.pocoo.org/docs/2.10/api/#jinja2.Markup) class or by using the `| safe` filter in the template.

Here is a basic introduction to how the Markup class works:

```python
>>> from flask import Markup
>>> Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'
Markup(u'<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>')
>>> Markup.escape('<blink>hacker</blink>')
Markup(u'&lt;blink&gt;hacker&lt;/blink&gt;')
>>> Markup('<em>Marked up</em> &raquo; HTML').striptags()
u'Marked up \xbb HTML'
```

## Context Locals
In Flask this information is provided by the global `request` object. If you have some experience with `Python` you might be wondering how that object can be global and how Flask manages to still be threadsafe. The answer is [context locals](http://flask.pocoo.org/docs/1.0/quickstart/#context-locals).

## The Request Object
[request](http://flask.pocoo.org/docs/1.0/api/#flask.Request)

### form
```python
from flask import request

@app.route('/login', methods=['POST', 'GET'])
def login():
  error = None
  if request.method == 'POST':
    if valid_login(request.form['username'],
      request.form['password']):
      return log_the_user_in(request.form['username'])
    else:
      error = 'Invalid username/password'

  # the code below is executed if the request method
  # was GET or the credentials were invalid
  return render_template('login.html', error=error)
```

### File Uploads
You can handle uploaded files with Flask easily. Just make sure not to forget to set the `enctype="multipart/form-data"` attribute on your HTML form, otherwise the browser will not transmit your files at all.

[uploading-files](http://flask.pocoo.org/docs/1.0/patterns/fileuploads/#uploading-files)

```python
from flask import request
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    print(request.files)
    f = request.files['the_file']
    f.save('/var/www/uploads/' + secure_filename(f.filename))
```

## Cookies

+ Reading cookies:
```python
from flask import request

@app.route('/')
def index():
  username = request.cookies.get('username')
  # use cookies.get(key) instead of cookies[key] to not get a
  # KeyError if the cookie is missing.
```

+ Storing cookies:
```python
from flask import make_response

@app.route('/')
def index():
  resp = make_response(render_template(...))
  resp.set_cookie('username', 'the username')
  return resp
```

## Redirects and Errors
To redirect a user to another endpoint, use the [redirect()](http://flask.pocoo.org/docs/1.0/api/#flask.redirect) function; to abort a request early with an error code, use the [abort()](http://flask.pocoo.org/docs/1.0/api/#flask.abort) function:

```python
from flask import abort, redirect, url_for

@app.route('/')
def index():
  return redirect(url_for('login'))

@app.route('/login')
def login():
  abort(401)
  this_is_never_executed()
```

By default a black and white error page is shown for each error code. If you want to customize the error page, you can use the `errorhandler()` decorator:
```python
from flask import render_template

@app.errorhandler(404)
def page_not_found(error):
  return render_template('page_not_found.html'), 404
```
See [Error handlers](http://flask.pocoo.org/docs/1.0/errorhandling/#error-handlers) for more details.

## Response
The return value from a view function is automatically converted into a response object for you. If the return value is a string it’s converted into a response object with the string as response body, a `200` OK status code and a *text/html* mimetype. The logic that Flask applies to converting return values into response objects is as follows:

1. If a response object of the correct type is returned it’s directly returned from the view.
2. If it’s a string, a response object is created with that data and the default parameters.
3. If a tuple is returned the items in the tuple can provide extra information. Such tuples have to be in the form `(response, status, headers)` or `(response, headers)` where at least one item has to be in the tuple. The status value will override the status code and headers can be a list or dictionary of additional header values.
4. If none of that works, Flask will assume the return value is a valid WSGI application and convert that into a response object.

If you want to get hold of the resulting response object inside the view you can use the [make_response()](http://flask.pocoo.org/docs/1.0/api/#flask.make_response) function.
```python flask
@app.errorhandler(404)
def not_found(error):
  resp = make_response(render_template('error.html'), 404)
  resp.headers['X-Something'] = 'A value'
  return resp
```

## Sessions
In addition to the request object there is also a second object called session which allows you to store information specific to a user from one request to the next. This is implemented on top of cookies for you and signs the cookies cryptographically. What this means is that the user could look at the contents of your cookie but not modify it, unless they know the secret key used for signing.

In order to use sessions you have to set a secret key. Here is how sessions work:

```python
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
```

### How to generate good secret keys
A secret key should be as random as possible. Your operating system has ways to generate pretty random data based on a cryptographic random generator. Use the following command to quickly generate a value for &&**Flask.secret_key** (or SECRET_KEY):

```bash
python -c 'import os; print(os.urandom(16))'
```

## logging
```python
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')
```