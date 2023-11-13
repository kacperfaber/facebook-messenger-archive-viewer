from argparse import ArgumentParser
import os
import sys

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_path)

from api.app import App
from api.storage import Storage
from image.db import Db
from image.image_builder import create_image_builder


def build(args):
    password = args.password
    image = args.image
    verbose = args.verbose
    archive = args.archive
    image_builder = create_image_builder(image, password, echo=verbose)
    image_builder.build_image(archive_dir=archive)


def run(args):
    port = args.port
    hostname = args.host
    image = args.image
    password = args.password

    engine = Db.create_engine(image_name=image, password=password)
    Storage.set_db(Db(engine=engine))

    app = App()
    app.run(host=hostname, port=port)


parser = ArgumentParser()

subparsers = parser.add_subparsers(dest="build")

# build
build_parser = subparsers.add_parser("build")
build_parser.set_defaults(func=build)
build_parser.add_argument("--image", type=str, default=None, help="Image path")
build_parser.add_argument("--password", type=str, default=None, help="Image security password")
build_parser.add_argument("--archive", type=str, default=".", help="Archive directory that contain messages/ directory. Default: .")
build_parser.add_argument("--verbose", type=bool, default=False, help="Verbose")

# run
run_parser = subparsers.add_parser("run")
run_parser.set_defaults(func=run)
run_parser.add_argument("--image", type=str, default=None, help="Image path")
run_parser.add_argument("--password", type=str, default=None, help="Image security password.")
run_parser.add_argument("--host", type=str, default="localhost", help="String, Default: localhost")
run_parser.add_argument("--port", type=int, default=8080, help="Integer, default: 8080")

a = parser.parse_args()
a.func(a)
