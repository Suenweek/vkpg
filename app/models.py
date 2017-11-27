from flask import session


class VkUser(object):
    """
    Represents a user
    """
    def __init__(self, access_token):
        self.access_token = access_token

    def __repr__(self):
        return "<VkUser()>"

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
        return self.access_token

    @property
    def access_token(self):
        return session["access_token"]

    @access_token.setter
    def access_token(self, value):
        session["access_token"] = value
