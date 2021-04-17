from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from utils.socket import socket
from flask_socketio import SocketIO, emit
from resources.repo import Repos
from resources.org import Org
from utils import clone, create_repos, clear_dir
import time
app = Flask(__name__)
CORS(app)
app.debug = True
app.env = 'development'

api = Api(app)

api.add_resource(Repos, '/repos')
api.add_resource(Org, '/orgs')


@socket.on('connect')
def connected():
    print('Connected')


@socket.on('message')
def get_message(message):
    print(message)
    pass


@socket.on('disconnect')
def disconnect():
    print('Disconnected')


@socket.on('StartUpload', namespace='/upload')
def init_upload(message):
    repos = message['repos']
    token = message['token']
    target = message['targetOrg']
    upload = clone(repos, target, token)
    create_repos(upload[0], token, target)
    emit('UploadProgress-{}'.format(token), {"status": "Finished"})
    clear_dir(upload[1])


if __name__ == '__main__':
    socket.init_app(app, async_mode='threading', cors_allowed_origins='*')
    app.run()
