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

    user = VkUser.create(
        user_id=response["user_id"],
        access_token=response["access_token"]
    )

    if user is not None:
        login_user(user)
        flash("Successfully logged in", category="success")
        return redirect(next_url)
    else:
        flash("Was not able log you in, try again later", category="danger")
        return redirect(next_url)


@login_required
@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out", category="info")
    return redirect(url_for("index"))


@app.route("/", methods=["GET", "POST"])
def index():
    form = DownloadForm()
    if form.validate_on_submit():
        access_token = current_user.access_token if current_user.is_authenticated else ""
        vkpg = VkPhotoGetter(access_token=access_token)
        try:
            vkpg.get_album(url=form.album_url.parsed)
        except Exception as e:
            app.logger.exception(e)
            flash(str(e), category="danger")
    return render_template("index.html", form=form)
