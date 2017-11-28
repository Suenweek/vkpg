import os
from multiprocessing import Pool
import vk
import requests
from .utils import offset_range
from .config import VK_API_VERSION, ALBUMS_DIR, BASEDIR


MAX_PHOTOS_PER_REQUEST = 1000
NUM_PROCS = 32


class VkPhotoGetter(object):
    """
    Downloads photo albums from VK
    """
    def __init__(self, access_token):
        self.session = vk.Session(access_token=access_token)
        self.api = vk.API(session=self.session)

    def get_album(self, url):
        photos_total_count = self.count_album_photos(url)
        if not photos_total_count:
            raise ValueError("No album found or album is empty")
        photos = self.get_album_photos(url, photos_total_count)
        pool = Pool(NUM_PROCS)
        pool.map(save_photo, photos)
        pool.close()
        pool.join()
        # TODO: Gzip album
        return os.path.join(BASEDIR, "app", "static", "img", "anon_50x50.png")

    def count_album_photos(self, url):
        return self.api.photos.get(
            owner_id=url.owner_id,
            album_id=url.album_id,
            count=0,
            v=VK_API_VERSION
        ).get("count")

    def get_album_photos(self, url, photos_total_count):
        for offset, count in offset_range(photos_total_count, count_max=MAX_PHOTOS_PER_REQUEST):
            bunch = self.api.photos.get(
                owner_id=url.owner_id,
                album_id=url.album_id,
                offset=offset,
                count=count,
                v=VK_API_VERSION
            )
            for item in bunch["items"]:
                yield self.find_largest_photo(item)

    def find_largest_photo(self, photo):
        max_key = max([key for key in photo.keys() if key.startswith("photo")],
                      key=lambda size: int(size.split("_")[-1]))
        return photo[max_key]


def save_photo(url, path=ALBUMS_DIR):
    with open(os.path.join(path, "%s.jpg") % hash(url), "wb") as f:
        f.write(requests.get(url).content)
