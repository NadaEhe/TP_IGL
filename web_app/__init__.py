
import os
import pathlib
from flask import Flask, abort, session,redirect, request, url_for
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
import google_auth_oauthlib
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from google.oauth2 import id_token
import google.auth.transport.requests
import requests
def create_app():
    app=Flask(__name__)
####authentification avec google SET UP##########
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    GOOGLE_CLIENT_ID="783422700642-2u6p1uacpi22g4gs2ki0ki7sg3gh9s6b.apps.googleusercontent.com"
    client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
    flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file, scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:7000/callback")

##############FIN DE SET UP#####################

#IMPORTING VIEW-------------------
    from .views import views
    app.register_blueprint(views, url_prefix='/') #registering the views all the groups of url
#FIN------------------------------
########CONGIGURATION DE L'APP--------------------------
    app.config['SECRET_KEY']= 'gbdfbknaz&é&²'
#-------------------------------------------------------

#########LOGIN REQUIRED SETUP--------------
    def login_is_required(function):
     def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
     return wrapper
########FIN de LOGIN REQUIRED--------------

    @app.route('/login')
    def login():
         authorization_url, state = flow.authorization_url()
         session["state"] = state
         return redirect(authorization_url)
    
    @app.route("/callback") #to receive data from google 
    def callback():
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
          abort(500)  # State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)
        id_info = id_token.verify_oauth2_token(id_token=credentials._id_token,  request=token_request,audience=GOOGLE_CLIENT_ID )

        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        return redirect(url_for('views.wrapper'))


    @app.route('/logout')
    def logout():
        session.clear
        return  redirect(url_for('views.index'))



    return app