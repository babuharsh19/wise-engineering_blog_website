from flask_login import LoginManager
from flask import Flask,Blueprint
from flask import Flask
app = Flask(__name__)
core = Blueprint('core',__name__)

loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_message = u"Please login to access this page"
loginmanager.login_message_category = "info"
app.register_blueprint(core)