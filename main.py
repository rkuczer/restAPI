from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('title', required=True)

videos = {
    'video1': {'title': 'Tequila, Lime Juice, Cointreau'},
    'video2': {'title': 'Bourbon, Angostura Bitters, Sugar, Orange Peel'},
    'video3': {'title': 'Rum, Mint, Lime Juice, Sugar, Club Soda'}
}


class Video(Resource):
    def get(self, videoID):
        if videoID == "all":
            return videos
        if videoID not in videos:
            abort(404, message=f"Video {videoID} not found.")

        return videos[videoID], 201

    def put(self, videoID):
        args = parser.parse_args()
        new_video = {'title': args['title']}
        videos[videoID] = new_video
        return {videoID: videos[videoID]}, 201 #good status code

    def delete(self, videoID):
        if videoID not in videos:
            abort(404, message=f"Video {videoID} not found.")
        del videos[videoID]
        return " ", 204

class VideoSchedule(Resource):
    def get(self):
        return videos
    def post(self):
        args = parser.parse_args()
        new_video = {'title' : args['title']}
        videoID = max(int(v.lstrip('video')) for v in videos.keys()) + 1
        videos[videoID] = new_video
        return videos[videoID], 201

api.add_resource(VideoSchedule, '/videos ')
api.add_resource(Video, '/videos/<videoID>')

if __name__ == '__main__':
    app.run()
