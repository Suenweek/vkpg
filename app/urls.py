import re
from urllib.parse import urlparse


class VkAlbumUrl(object):
    """
    Represents vk url for a photo album
    """
    def __init__(self, url):
        self.regex = re.compile(r"/album(\-{0,1}\d+)_(\d+)")
        self.owner_id, self.album_id = self.parse(url)

    def __str__(self):
        return "<VkAlbumUrl(owner_id='%s', album_id='%s')>" % (self.owner_id, self.album_id)

    def parse(self, url):
        path = urlparse(url).path
        search = self.regex.search(path)
        if search is not None:
            return search.groups()
        else:
            raise ValueError("Invalid album url")
