from argparse import ArgumentParser
from app import app
import webbrowser


def main(args):
    if args.browser_needed:
        webbrowser.open("http://127.0.0.1:%d" % args.port)
    app.run(port=args.port, debug=args.debug)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("port", nargs="?", type=int, default=5000)
    arg_parser.add_argument("-d", "--debug", dest="debug", action="store_true")
    arg_parser.add_argument("-nb", "--no-browser", dest="browser_needed", action="store_false")
    main(arg_parser.parse_args())
