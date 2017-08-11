from flask import Flask, request
from flask_restful import Resource, Api
from omxplayer import OMXPlayer
from omxplayer.keys import HIDE_VIDEO, UNHIDE_VIDEO


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


class TiledPlayers(object):
    def __init__(self):
        self.c1 = "rtsp://admin:12345678@192.168.10.240:554/cam/realmonitor?channel=1&subtype=1"
        self.c2 = "rtsp://admin:12345678@192.168.10.241:554/cam/realmonitor?channel=1&subtype=1"
        self.c3 = "rtsp://admin:12345678@192.168.10.242:554/cam/realmonitor?channel=1&subtype=1"
        self.c4 = "rtsp://admin:12345678@192.168.10.243:554/cam/realmonitor?channel=1&subtype=1"
        self.c5 = "rtsp://admin:12345678@192.168.10.244:554/cam/realmonitor?channel=1&subtype=1"
        self.p1 = OMXPlayer(
            self.c1,
            args=[
                '--avdict="rtsp_transport:tcp"',
                '--threshod=.01',
                '--video_fifo=.01',
                '--win=16,0,368,288'
            ]
        )
        self.p2 = OMXPlayer(
            self.c2,
            args=[
                '--avdict="rtsp_transport:tcp"',
                '--threshod=.01',
                '--video_fifo=.01',
                '--layer=1',
                '--win=400,0,752,288'
            ]
        )
        self.p3 = OMXPlayer(
            self.c3,
            args=[
                '--avdict="rtsp_transport:tcp"',
                '--threshod=.01',
                '--video_fifo=.01',
                '--layer=1',
                '--win=784,0,1136,288'
            ]
        )
        self.p4 = OMXPlayer(
            self.c4,
            args=[
                '--avdict="rtsp_transport:tcp"',
                '--threshod=.01',
                '--video_fifo=.01',
                '--layer=1',
                '--win=1168,0,1520,288'
            ]
        )
        self.p5 = OMXPlayer(
            self.c5,
            args=[
                '--avdict="rtsp_transport:tcp"',
                '--threshod=.01',
                '--video_fifo=.01',
                '--layer=1',
                '--win=1552,0,1904,288'
            ]
        )

    def hide_all(self):
        self.p1.action(HIDE_VIDEO)
        self.p2.action(HIDE_VIDEO)
        self.p3.action(HIDE_VIDEO)
        self.p4.action(HIDE_VIDEO)
        self.p5.action(HIDE_VIDEO)
        return True

    def unhide_all(self):
        self.p1.action(UNHIDE_VIDEO)
        self.p2.action(UNHIDE_VIDEO)
        self.p3.action(UNHIDE_VIDEO)
        self.p4.action(UNHIDE_VIDEO)
        self.p5.action(UNHIDE_VIDEO)
        return True


app = Flask(__name__)
api = Api(app)

player = OMXPlayer(
    streams[0],
    args=[
        '--avdict="rtsp_transport:tcp"',
        '--threshold=.01',
        '--video_fifo=.01',
        '--fps=15',
        '--layer=2'
    ]
)

current_cam = 0
tiles = TiledPlayers()


class CameraStream(Resource):
    def get(self, cam_num):
        if current_cam == cam_num:
            return {'stream': cam_num}
        else:
            player.load(streams[cam_num])
            return {'stream': cam_num}


class CameraTile(Resource):
    def get(self, action):
        if action == 'tile':
            player.action(HIDE_VIDEO)
            tiles.unhide_all()
            return {'stream': 'tiled'}
        else:
            player.action(UNHIDE_VIDEO)
            tiles.hide_all()
            return {'stream': 'not_tiled'}


api.add_resource(CameraStream, '/cam/<int:cam_num>')
api.add_resource(CameraTile, '/cam/<string:action>')


if __name__ == '__main__':
    player.load(streams[0])
    app.run(host='0.0.0.0')

