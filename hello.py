from flask import Flask, url_for, request, flash, redirect, render_template, Markup
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
  return "<h1>hi, Nice guy</h1>"

@app.route('/hello')
def hello():
  return 'Hello, World'

@app.route('/login', methods=['GET', 'POST'])
def login():
  print(request) # request is a dict. it has `path`, `method`, `form` ...
  def valid_login(username, password):
    if username != None and isinstance(username, str):
      return True
    else:
      raise TypeError('username is not a valid string, it is %s' % username)

    if password != None and isinstance(password, str):
      return True
    else:
      raise TypeError('password is not a valid string, it is %s' % password)

  error = None
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    if valid_login(username, password):
      return render_template('login.html', username=username)
    else:
      error = 'Invalid username/password'

  # the code below is executed if the request method
  # was GET or the credentials were invalid
  return render_template('login.html', error=error)

@app.route('/profile')
def profile():
  return 'Welcome to look you profile, guy!'

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

@app.route('/express/<string:words>')
def show_words(words):
  return 'That\'s the all words \'%s\' what u wanna say, right?' % words

@app.route('/projects/')
def projects():
  return 'The project page'

@app.route('/about')
def about():
  return 'The about page'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('uploaded_file', filename=filename))

with app.test_request_context():
  print(url_for('index'))
  print(url_for('login'))
  print(url_for('login', next='/'))
  print(url_for('profile', username='John Doe'))

# RESTful API
