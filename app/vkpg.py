import os
from multiprocessing import Pool, Process
import webbrowser
from functools import partial
import vk
import requests
from .utils import offset_range
from .config import VK_API_VERSION, ALBUMS_DIR


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
        # Count photos
        photos_total_count = self.count_album_photos(url)
        if not photos_total_count:
            raise ValueError("No album found or album is empty")

        # Setup album path
        album_path = os.path.join(ALBUMS_DIR, self.get_album_name(url))
        if not os.path.exists(album_path):
            os.mkdir(album_path)

        # Get photos generator
        photos = self.get_album_photos(url, photos_total_count)

        # Download photos using multiprocessing
        Process(
            target=save_all_photos,
            args=(photos, album_path)
        ).start()

        # Open result in explorer/nautilus/whatever
        webbrowser.open("file://%s" % album_path)

    def count_album_photos(self, url):
        return self.api.photos.get(
            owner_id=url.owner_id,
            album_id=url.album_id,
            count=0,
            v=VK_API_VERSION
        ).get("count")

    def get_album_name(self, url):
        # TODO: Get actual name
        return "name"

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
        max_key = max([key for key in photo.keys()
                       if key.startswith("photo_")],
                      key=lambda size: int(size.split("_")[-1]))
        return photo[max_key]


def save_photo(url, album_path):
    filename = os.path.join(album_path, "%s.jpg" % hash(url))
    with open(filename, "wb") as f:
        f.write(requests.get(url).content)


def save_all_photos(photos, album_path):
    pool = Pool(NUM_PROCS)
    pool.map(partial(save_photo, album_path=album_path), photos)
    pool.close()
    pool.join()
