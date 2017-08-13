from __future__ import print_function

from flask import Flask, request
from flask_restful import Resource, Api
from omxplayer import OMXPlayer
from omxplayer.keys import HIDE_VIDEO, UNHIDE_VIDEO, PAUSE

import time


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

sub_streams = [
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


sub_stream1 = OMXPlayer(
    sub_streams[3],
    args=[
        "--layer=20",
        "--threshold=0",
        "--video_fifo=0",
        "--timeout=0",
        "--genlog",
        "--win=1280,60,1920,540",
        "--avdict=rtsp_transport:tcp"
    ]
)

sub_stream2 = OMXPlayer(
    sub_streams[2],
    args=[
        "--layer=20",
        "--threshold=0",
        "--video_fifo=0",
        "--timeout=0",
        "--genlog",
        "--win=1280,540,1920,1020",
        "--avdict=rtsp_transport:tcp"
    ]
)

# sub_stream2 = OMXPlayer(
#     sub_streams[2],
#     args=[
#         "--layer=20",
#         "--threshold=0",
#         "--video_fifo=0",
#         "--timeout=0",
#         "--genlog",
#         "--win=352,0,704,288",
#         "--avdict=rtsp_transport:tcp"
#     ]
# )

rtsp_feed = OMXPlayer(
    streams[0],
    args=[
        "--layer=20",
        "--threshold=0",
        "--video_fifo=0",
        "--timeout=0",
        "--genlog",
        "--win=0,180,1280,900",
        "--avdict=rtsp_transport:tcp"
    ]
)


def get_player(stream_num):
    p = OMXPlayer(
        streams[stream_num],
        dbus_name="org.mpris.MediaPlayer2.omxplayer%s" % stream_num,
        args=[
            "--layer=20",
            "--threshold=0",
            "--video_fifo=0",
            "--timeout=0",
            "--genlog",
            "--win=0,180,1280,900",
            "--avdict=rtsp_transport:tcp",
            "--dbus_name=org.mpris.MediaPlayer2.omxplayer%s" % stream_num
        ]
    )
    return p

# players = []
#
# for i in range(len(streams)):
#     dbus_id = "org.mpris.MediaPlayer2.omxplayer%s" % i
#     player = None
#     if i == 0:
#         player = OMXPlayer(
#             streams[i],
#             dbus_name="org.mpris.MediaPlayer2.omxplayer",
#             args=[
#                 #"--blank",
#                 "--layer=%s" % i,
#                 "--live",
#                 "--threshold=0.8",
#                 "--video_fifo=1",
#                 "--timeout=0",
#                 "--genlog",
#                 "--win=-1920,-1080,0,0"
#                 "--dbus_name=org.mpris.MediaPlayer2.omxplayer"
#             ]
#         )
#     else:
#         player = OMXPlayer(
#             streams[i],
#             dbus_name=dbus_id,
#             args=[
#                 #"--blank",
#                 "--layer=%s" % i,
#                 "--live",
#                 "--threshold=0.8",
#                 "--video_fifo=1",
#                 "--timeout=0",
#                 "--dbus_name=%s" % dbus_id,
#                 "--win=-1920,-1080,0,0",
#                 "--genlog"
#             ]
#         )
        # time.sleep(5)
        # pb_status = player.playback_status() == "Playing"
        # while not pb_status:
        #     print("Player %s not playing, attempting restart" % i)
        #     player.quit()
        #     time.sleep(2)
        #     player = OMXPlayer(
        #         streams[i],
        #         dbus_name=dbus_id,
        #         args=[
        #             "--layer=%s" % i,
        #             "--threshold=0",
        #             "--video_fifo=0",
        #             "--timeout=0",
        #             "--dbus_name=%s" % dbus_id,
        #             "--win=-1920,-1080,0,0"
        #             "--genlog"
        #         ]
        #     )
        #     time.sleep(10)
        #     pb_status = player.playback_status() == "Playing"

    # print("Started player: %s" % i)
    # time.sleep(5)
    # players.append(player)


current_cam = 0


class CameraStream(Resource):
    def get(self, cam_num):
        global current_cam
        global rtsp_feed

        if cam_num != current_cam:
            new_feed = get_player(cam_num)
            time.sleep(0.5)
            rtsp_feed.quit()
            rtsp_feed = new_feed
            current_cam = cam_num

        return {'stream': current_cam}



# class CameraStream(Resource):
#     def get(self, cam_num):
#         global current_cam
#         global players
#         players[current_cam].set_video_pos(-1920, -1080, 0, 0)
#         time.sleep(0.5)
#         players[cam_num].set_video_pos(0, 0, 1920, 1080)
#         current_cam = cam_num
#         return {'stream': cam_num}
#
#
# class CameraStatus(Resource):
#     def get(self, cam_num, action):
#         global players
#         if action == "pause":
#             players[cam_num].pause()
#         elif action == "play":
#             players[cam_num].play()
#         elif action == "refresh":
#             players[cam_num].pause()
#             time.sleep(1)
#             players[cam_num].play()
#         return {'stream': cam_num}




app = Flask(__name__)
api = Api(app)

api.add_resource(CameraStream, '/cam/<int:cam_num>')
# api.add_resource(CameraStatus, '/control/<int:cam_num>/<string:action>')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

