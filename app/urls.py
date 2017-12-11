import re
from urllib.parse import urlparse


class VkAlbumUrl(object):
    """
    Represents vk url for a photo album
    """
    REGEX = re.compile(r"/album(\-{0,1}\d+)_(\d+)")

    def __init__(self, url):
        groups = self.parse(url)
        self.owner_id = self.parse_owner_id(groups[0])
        self.album_id = self.parse_album_id(groups[1])

    def __str__(self):
        return "<VkAlbumUrl(owner_id='%s', album_id='%s')>" % (self.owner_id, self.album_id)

    def parse(self, url):
        path = urlparse(url).path
        search_result = VkAlbumUrl.REGEX.search(path)
        if search_result is not None:
            return search_result.groups()
        else:
            raise ValueError("Invalid album url")

    def parse_owner_id(self, owner_id):
        return owner_id

    def parse_album_id(self, album_id):
        return {
            "0": "profile",
            "00": "wall",
            "000": "saved"
        }.get(album_id, album_id)
