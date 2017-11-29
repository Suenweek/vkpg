import sys
from flask import g, redirect, url_for, request, render_template, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_oauthlib.client import OAuthException
from . import app, vk_oauth, lm
from .forms import DownloadForm
from .models import VkUser
from .vkpg import VkPhotoGetter


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(user_id):
    return VkUser.get(user_id)


@app.route("/login/oauth/vk")
def login_oauth_vk():
    if app.config["VK_APP_PARAMS_SET"]:
        next_url = request.args.get("next") or request.referrer or None
        callback_url = url_for("callback_oauth_vk", next=next_url, _external=True)
        return vk_oauth.authorize(callback=callback_url)

    flash("Login feature is not available as no VK app parameters set. "
          "Consult %s for solution." % app.config["REPO_URL"],
          category="warning")
    return redirect(url_for("index"))


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
        app.logger.info("%s denied request to sign in", current_user)
        flash("You denied the request to sign in", category="warning")
        return redirect(next_url)

    user = VkUser.create(
        user_id=response["user_id"],
        access_token=response["access_token"]
    )
    if user is not None:
        app.logger.info("Logging in %s", user)
        login_user(user)
        flash("Successfully logged in", category="success")
    else:
        app.logger.error("Was not able to login %s", user)
        flash("Was not able log you in, try again later", category="danger")
    return redirect(next_url)


@app.route("/logout")
@login_required
def logout():
    next_url = request.args.get("next") or url_for("index")
    app.logger.info("Logging out %s", current_user)
    logout_user()
    flash("Logged out", category="info")
    return redirect(next_url)


@app.route("/shutdown")
def shutdown():
    if current_user.is_authenticated:
        return redirect(url_for("logout", next=url_for("shutdown")))
    app.logger.info("<== Shutting down... ==>")
    sys.exit(0)


@app.route("/", methods=["GET", "POST"])
def index():
    form = DownloadForm()
    if form.validate_on_submit():
        access_token = current_user.access_token if current_user.is_authenticated else ""
        vkpg = VkPhotoGetter(access_token=access_token)
        try:
            app.logger.info("Downloading %s", form.album_url.parsed)
            vkpg.get_album(url=form.album_url.parsed)
            flash("Album downloaded", category="success")
        except Exception as e:
            app.logger.exception(e)
            flash(str(e), category="danger")
    return render_template("index.html", form=form)
