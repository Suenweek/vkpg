import vk
from flask import session
from . import app


class VkUser(object):
    """
    Represents a user
    """
    __slots__ = ("user_id", "access_token", "name", "avatar_url")

    def __init__(self, user_id, access_token=None, name=None, avatar_url=None):
        self.user_id= user_id
        if access_token is not None:
            self.access_token = access_token
        if name is not None:
            self.name = name
        if avatar_url is not None:
            self.avatar_url = avatar_url

    def __repr__(self):
        return "<VkUser(name='%s')>" % self.name

    def __setattr__(self, key, value):
        session[key] = value

    def __getattr__(self, item):
        return session.get(item)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    @classmethod
    def create(cls, user_id, access_token):
        # Getting api object
        vk_session = vk.Session(access_token)
        vk_api = vk.API(vk_session)

        # Sending request
        response = vk_api.users.get(
            users_ids=user_id,
            fields="photo_50",
            version=app.config["VK_API_VERSION"]
        )

        # Parsing response
        if len(response) != 1:
            app.logger.error("Unexpected vk response while updating "
                             "vk user info: %s" % response)
            return None
        vk_user_info = response[0]

        # Name
        first_name = vk_user_info.get("first_name")
        last_name = vk_user_info.get("last_name")
        # If both names are not None
        if not (first_name is None or last_name is None):
            name = "%s %s" % (first_name, last_name)
        else:
            name = app.config["VK_USER_DEFAULT_NAME"]

        # Avatar
        avatar_url = vk_user_info.get("photo_50", app.config["VK_USER_DEFAULT_AVATAR_URL"])

        return cls(
            user_id=user_id,
            access_token=access_token,
            name=name,
            avatar_url=avatar_url
        )

    @classmethod
    def get(cls, user_id):
        if session.get("user_id") == user_id:
            return cls(user_id)
