from flask import Flask, request
from flask_restful import Resource, Api
from omxplayer import OMXPlayer
from omxplayer.keys import *

import socket
import time
import subprocess
import multiprocessing
import urllib.parse
import logging

streams = [
    "rtsp://admin:12345678@192.168.10.240:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:12345678@192.168.10.241:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:12345678@192.168.10.242:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:12345678@192.168.10.243:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:12345678@192.168.10.244:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:12345678@192.168.10.245:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:12345678@192.168.10.246:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:12345678@192.168.10.247:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:12345678@192.168.10.248:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:12345678@192.168.10.249:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://192.168.10.170:554/stander/livestream/0/1",
    "rtsp://192.168.10.171:554/stander/livestream/0/1"
]

app = Flask(__name__)
api = Api(app)

player = OMXPlayer(streams[0], args=['--no-osd', '--live'])


class CameraStream(Resource):
    def get(self, cam_num):
        player.load(streams[cam_num])
        return {'stream': streams[cam_num]}


api.add_resource(CameraStream, '/cam/<string:cam_num>')


if __name__ == '__main__':
    app.run()

