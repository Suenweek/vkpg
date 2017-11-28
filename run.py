from argparse import ArgumentParser
from app import app


HOST = "127.0.0.1"
PORT = 5000


def main(args):
    app.run(HOST, PORT)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    main(arg_parser.parse_args())
