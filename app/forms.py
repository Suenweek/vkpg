from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired
from .urls import VkAlbumUrl


class DownloadForm(FlaskForm):
    """
    Form for submitting an album to be downloaded
    """
    album_url = StringField(
        "Album url",
        validators=[DataRequired()]
    )
    submit = SubmitField("Download")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        else:
            try:
                self.album_url.parsed = VkAlbumUrl(self.album_url.data)
                return True
            except ValueError as e:
                self.album_url.errors.append(str(e))
                return False
