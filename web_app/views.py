from flask import Blueprint, abort, session
def login_is_required(function): # equivalent l login_required from flask_login
     def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

     return wrapper
views=Blueprint('views',__name__)
@views.route("/")
def index():
       return "Hello World <a href='/login'><button>Login</button></a>"

@views.route("/hello")
@login_is_required
def hello():
      return "Hello NADA YOU DID IT !! <a href='/logout'><button>Logout</button></a>"   #f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"