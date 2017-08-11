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

player = OMXPlayer(
    streams[0],
    args=[
        '--avdict="rtsp_transport:tcp"',
        '--threshold=0',
        '--video_fifo=0',
        '--fps=15',
        '--layer=2',
        '--live'
    ]
)

# c1 = "rtsp://admin:12345678@192.168.10.240:554/cam/realmonitor?channel=1&subtype=1"
# c2 = "rtsp://admin:12345678@192.168.10.241:554/cam/realmonitor?channel=1&subtype=1"
# c3 = "rtsp://admin:12345678@192.168.10.242:554/cam/realmonitor?channel=1&subtype=1"
# c4 = "rtsp://admin:12345678@192.168.10.243:554/cam/realmonitor?channel=1&subtype=1"
# c5 = "rtsp://admin:12345678@192.168.10.244:554/cam/realmonitor?channel=1&subtype=1"
# p1 = OMXPlayer(
#     c1,
#     args=[
#         '--avdict="rtsp_transport:tcp"',
#         '--threshold=.01',
#         '--video_fifo=.01',
#         '--win="16 0 368 288"'
#     ]
# )
# p2 = OMXPlayer(
#     c2,
#     args=[
#         '--avdict="rtsp_transport:tcp"',
#         '--threshold=.01',
#         '--video_fifo=.01',
#         '--layer=1',
#         '--win="400 0 752 288"'
#     ]
# )
# p3 = OMXPlayer(
#     c3,
#     args=[
#         '--avdict="rtsp_transport:tcp"',
#         '--threshold=.01',
#         '--video_fifo=.01',
#         '--layer=1',
#         '--win="784 0 1136 288"'
#     ]
# )
# p4 = OMXPlayer(
#     c4,
#     args=[
#         '--avdict="rtsp_transport:tcp"',
#         '--threshold=.01',
#         '--video_fifo=.01',
#         '--layer=1',
#         '--win="1168 0 1520 288"'
#     ]
# )
# p5 = OMXPlayer(
#     c5,
#     args=[
#         '--avdict="rtsp_transport:tcp"',
#         '--threshold=.01',
#         '--video_fifo=.01',
#         '--layer=1',
#         '--win="1552 0 1904 288"'
#     ]
# )
#
#
# def hide_all():
#     p1.action(HIDE_VIDEO)
#     p2.action(HIDE_VIDEO)
#     p3.action(HIDE_VIDEO)
#     p4.action(HIDE_VIDEO)
#     p5.action(HIDE_VIDEO)
#     return True
#
#
# def unhide_all():
#     p1.action(UNHIDE_VIDEO)
#     p2.action(UNHIDE_VIDEO)
#     p3.action(UNHIDE_VIDEO)
#     p4.action(UNHIDE_VIDEO)
#     p5.action(UNHIDE_VIDEO)
#     return True

current_cam = 0


class CameraStream(Resource):
    def get(self, cam_num):
        if current_cam == cam_num:
            return {'stream': cam_num}
        else:
            player.load(streams[cam_num])
            return {'stream': cam_num}


# class CameraTile(Resource):
#     def get(self, action):
#         if action == 'tile':
#             # player.action(HIDE_VIDEO)
#             unhide_all()
#             return {'stream': 'tiled'}
#         else:
#             # player.action(UNHIDE_VIDEO)
#             hide_all()
#             return {'stream': 'not_tiled'}


app = Flask(__name__)
api = Api(app)

api.add_resource(CameraStream, '/cam/<int:cam_num>')
# api.add_resource(CameraTile, '/cam/<string:action>')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

