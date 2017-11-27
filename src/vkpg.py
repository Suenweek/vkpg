import vk
from .utils import offset_range


class VkPhotoGetter(object):

    def __init__(self, session=None):
        self.api = vk.API(session=session)

    def get_album(self, url):
        pass

    def count_album_photos(self, url):
        pass
