from flask import g, redirect, url_for, request, render_template, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_oauthlib.client import OAuthException
from . import app, vk_oauth, lm
from .models import VkUser


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(access_token):
    return VkUser(access_token=access_token)


@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        next_url = request.args.get("next") or url_for("index")
        return redirect(url_for("login_oauth_vk", next=next_url))


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out", category="info")
    return redirect(url_for("index"))


@app.route("/login/oauth/vk")
def login_oauth_vk():
    next_url = request.args.get("next") or request.referrer or None
    callback_url = url_for("callback_oauth_vk", next=next_url, _external=True)
    return vk_oauth.authorize(callback=callback_url)


@app.route("/callback/oauth/vk")
def callback_oauth_vk():
    next_url = request.args.get("next") or url_for("index")

    try:
        response = vk_oauth.authorized_response()
    except OAuthException as e:
        app.logger.exception(e)
        flash("Was not able log you in, try again later", category="danger")
        return redirect(next_url)

    if response is None:
        flash("You denied the request to sign in", category="warning")
        return redirect(next_url)

    user = VkUser(access_token=response["access_token"])
    login_user(user)

    flash("Successfully logged in", category="success")
    return redirect(next_url)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@login_required
@app.route("/download", methods=["GET", "POST"])
def download():
    return render_template("download.html")
