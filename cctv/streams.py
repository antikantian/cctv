from flask import Flask, request
from flask_restful import Resource, Api
from omxplayer import OMXPlayer
from omxplayer.keys import *


streams = [
    "rtsp://admin:12345678@192.168.10.240:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://admin:12345678@192.168.10.241:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://admin:12345678@192.168.10.242:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://admin:12345678@192.168.10.243:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://admin:12345678@192.168.10.244:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://admin:12345678@192.168.10.245:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://admin:12345678@192.168.10.246:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://admin:12345678@192.168.10.247:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://admin:12345678@192.168.10.248:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://admin:12345678@192.168.10.249:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://192.168.10.170:554/stander/livestream/0/0",
    "rtsp://192.168.10.171:554/stander/livestream/0/0"
]

app = Flask(__name__)
api = Api(app)

player = OMXPlayer(streams[0], args=['--avdict="rtsp_transport:tcp"', '--threshold=.01', '--video_fifo=.01', '--fps=15'])


class CameraStream(Resource):
    def get(self, cam_num):
        player.load(streams[cam_num])
        return {'stream': streams[cam_num]}


api.add_resource(CameraStream, '/cam/<int:cam_num>')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

