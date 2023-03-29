from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import json

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('uploadDate', type=int, required=False)

with open('videos.json', 'r') as f:
    videos = json.load(f)
def write_changes_to_file():
    global videos
    videos = {k: v for k, v in sorted(videos.items(), key=lambda video: video[1]['uploadDate'])}
    with open('videos.json', 'w') as file:
        json.dump(videos, file)

class Video(Resource):
    def get(self, videoID):
        if videoID == "all":
            return videos
        if videoID not in videos:
            abort(404, message=f"Video {videoID} not found.")
        return videos[videoID], 201

    def put(self, videoID):
        args = parser.parse_args()
        new_video = {'title': args['title'], 'uploadDate': args['uploadDate']}
        videos[videoID] = new_video
        write_changes_to_file()
        return {videoID: videos[videoID]}, 201  # good status code

    def delete(self, videoID):
        if videoID not in videos:
            abort(404, message=f"Video {videoID} not found.")
        del videos[videoID]
        write_changes_to_file()
        return " ", 204


class VideoSchedule(Resource):
    def get(self):
        return videos

    def post(self):
        args = parser.parse_args()
        new_video = {'title': args['title'], 'uploadDate': args['uploadDate']}
        videoID = max(int(v.lstrip('video')) for v in videos.keys()) + 1
        videoID = f"video{videoID}"
        videos[videoID] = new_video
        write_changes_to_file()
        return videos[videoID], 201


api.add_resource(Video, '/videos/<videoID>')
api.add_resource(VideoSchedule, '/videos ')

if __name__ == '__main__':
    app.run()
