from argparse import ArgumentParser
from app import app


def main(args):
    app.run("127.0.0.1", 5000)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    main(arg_parser.parse_args())
