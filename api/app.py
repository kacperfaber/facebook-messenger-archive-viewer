from flask import Flask

from api.conversation_controller import conversation_blueprint
from api.attachment_controller import attachment_blueprint


class App:
    blueprints = [attachment_blueprint, conversation_blueprint]

    def __init__(self):
        self.app = Flask(__name__)

    def __register_blueprints(self):
        [self.app.register_blueprint(bp) for bp in self.blueprints]

    def run(self, host="localhost", port=8080):
        self.__register_blueprints()
        self.app.run(host=host, port=port)
