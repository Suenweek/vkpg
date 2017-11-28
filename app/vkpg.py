import vk
from .utils import offset_range
from .config import VK_API_VERSION


MAX_PHOTOS_PER_REQUEST = 1000


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
        for offset, count in offset_range(photos_total_count, count_max=MAX_PHOTOS_PER_REQUEST):
            bunch = self.api.photos.get(
                owner_id=url.owner_id,
                album_id=url.album_id,
                offset=offset,
                count=count,
                v=VK_API_VERSION
            )
            for item in bunch["items"]:
                photo_url = self.find_largest_photo(item)
                raise NotImplementedError("TBD")

    def count_album_photos(self, url):
        return self.api.photos.get(
            owner_id=url.owner_id,
            album_id=url.album_id,
            count=0,
            v=VK_API_VERSION
        ).get("count")

    def find_largest_photo(self, photo):
        max_key = max([key for key in photo.keys() if key.startswith("photo")],
                      key=lambda size: int(size.split("_")[-1]))
        return photo[max_key]

    def save_photo(self, url):
        pass
