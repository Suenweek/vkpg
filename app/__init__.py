from flask import Flask
from flask_oauthlib.client import OAuth
from flask_login import LoginManager
from . import config


# App instance
app = Flask(__name__)

# Config
app.config.from_object(config)

# OAuth
oauth = OAuth(app)
vk_oauth = oauth.remote_app(
    "vk",
    request_token_params={"scope": app.config["VK_PERMISSIONS"]},
    base_url="https://api.vk.com/method/",
    request_token_url=None,
    access_token_url="https://oauth.vk.com/access_token",
    authorize_url="https://oauth.vk.com/authorize",
    app_key="VK"
)

# LoginManager
lm = LoginManager(app)
lm.login_view = "login"
lm.login_message_category = "warning"


from . import routes
