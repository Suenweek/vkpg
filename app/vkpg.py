import os
import webbrowser
import requests
import vk
from functools import partial
from tempfile import gettempdir
from multiprocessing.pool import ThreadPool
from .utils import offset_range, create_sleep_hook
from .config import VK_API_VERSION, APP_NAME


MAX_PHOTOS_PER_REQUEST = 1000
NUM_WORKERS = 8
RATE_LIMIT_SLEEP_TIME = 0.3


class VkPhotoGetter(object):
    """
    Downloads photo albums from VK
    """
    def __init__(self, access_token):
        self.session = vk.Session(access_token=access_token)
        self.session.requests_session.hooks["response"].append(
            create_sleep_hook(seconds=RATE_LIMIT_SLEEP_TIME)
        )
        self.api = vk.API(session=self.session)

    def get_album(self, url):
        # Count photos
        photos_total_count = self.count_album_photos(url)
        if photos_total_count == 0:
            raise ValueError("Album is empty")

        # Setup album path
        album_path = self._get_album_path(url)
        if not os.path.exists(album_path):
            os.mkdir(album_path)

        # Get photos urls
        photos = self.get_album_photos(url, photos_total_count)

        # Download and save
        self._save_all_photos(photos, album_path)

        # Open result in explorer/nautilus/whatever
        webbrowser.open("file://%s" % album_path)

    def count_album_photos(self, url):
        return self.api.photos.get(
            owner_id=url.owner_id,
            album_id=url.album_id,
            count=0,
            v=VK_API_VERSION
        ).get("count", 0)

    def _get_album_path(self, url):
        dir_name = "%s_album_%s_%s" % (APP_NAME, url.owner_id, url.album_id)
        return os.path.join(gettempdir(), dir_name)

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
                yield self._find_largest_photo(item)

    def _find_largest_photo(self, photo):
        max_key = max([key for key in photo.keys()
                       if key.startswith("photo_")],
                      key=lambda size: int(size.split("_")[-1]))
        return photo[max_key]

    def _save_all_photos(self, photos, album_path):
        save_photo = partial(self._save_photo, album_path=album_path)
        pool = ThreadPool(NUM_WORKERS)
        pool.map(save_photo, photos)
        pool.close()
        pool.join()

    def _save_photo(self, url, album_path):
        filename = os.path.join(album_path, "%s.jpg" % hash(url))
        with open(filename, "wb") as f:
            f.write(requests.get(url).content)
