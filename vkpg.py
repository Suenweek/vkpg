from argparse import ArgumentParser
from src.vkpg import VkPhotoGetter
from src.urls import VkAlbumUrl


def main(args):
    vkpg = VkPhotoGetter(session=None)
    vkpg.get_album(url=args.album_url)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument(dest="album_url", type=VkAlbumUrl)
    arg_parser.add_argument("-o", dest="output")
    main(arg_parser.parse_args())
