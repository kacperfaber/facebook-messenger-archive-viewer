from flask import Flask

from api.storage import Storage
from image.db import Db
from routes.attachment_controller import attachment_blueprint


class App:
    blueprints = [attachment_blueprint]

    def __init__(self):
        self.app = Flask(__name__)

    def __register_blueprints(self):
        [self.app.register_blueprint(bp) for bp in self.blueprints]

    def run(self, host="localhost", port=8080):
        self.__register_blueprints()
        self.app.run(host=host, port=port)


db = Db(Db.create_engine("/home/kacperfaber/Pulpit/karolka", password=None))
Storage.set_db(db)

if __name__ == '__main__':
    app = App()
    app.run()






