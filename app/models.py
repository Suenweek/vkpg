from flask import session


class VkUser(object):
    """
    Represents a user
    """
    def __init__(self, id, access_token=None):
        self.id = id
        if access_token is not None:
            self.access_token = access_token

    def __repr__(self):
        return "<User(id='%s')>" % self.id

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
        return self.id

    @property
    def access_token(self):
        return session["access_token"]

    @access_token.setter
    def access_token(self, value):
        session["access_token"] = value
