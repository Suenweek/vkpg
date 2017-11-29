import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_oauthlib.client import OAuth
from flask_login import LoginManager
from . import config


# App instance
app = Flask(__name__)

# Config
app.config.from_object(config)

# Logging
if app.debug:
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
handler = RotatingFileHandler(
    filename=config.LOG_PATH,
    mode="a",
    maxBytes=config.LOG_MAX_BYTES,
    backupCount=config.LOG_BAK_COUNT
)
handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
handler.setFormatter(logging.Formatter(config.LOG_FMT))
app.logger.addHandler(handler)

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
lm.login_view = "login_oauth_vk"
lm.login_message_category = "warning"


from . import routes
