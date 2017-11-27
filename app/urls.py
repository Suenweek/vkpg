import re
from urllib.parse import urlparse


class VkAlbumUrl(object):

    def __init__(self, url):
        self.regex = re.compile(r"/album(\d+)_(\d+)")
        self.owner_id, self.album_id = self.parse(url)

    def parse(self, url):
        path = urlparse(url).path
        return self.regex.search(path)
