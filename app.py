from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_socketio import SocketIO
from resources.repo import Repos
from resources.org import Org
app = Flask(__name__)
CORS(app)
app.debug = True
app.env = 'development'
app.config['environment'] = 'development'
socket = SocketIO(app, async_mode='threading', cors_allowed_origins='*')
api = Api(app)

api.add_resource(Repos, '/repos')
api.add_resource(Org, '/orgs')


# @socket.on('connected')
# def handle_message(data):
#     socket.emit('Hi')


@socket.on('connect')
def connected():
    print('Connected')


@socket.on('disconnect')
def disconnect():
    print('Disconnected')


@socket.on('hi')
def print_hi(message):
    print('hi, {message}'.format(message=message))


if __name__ == '__main__':
    socket.init_app(app, debug=True)
    # app.run()
