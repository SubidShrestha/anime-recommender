from flask import Flask,request
from flask_restful import Api, Resource
from main import get_recommendations,get_popular_anime,get_anime_from_anime_id
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class Anime(Resource):
    def get(self):
        id = request.args.get('id')
        if id is not None:
            anime = get_anime_from_anime_id(int(id))
            return anime
        animes = get_popular_anime()
        return animes
    
    def post(self):
        data = request.get_json()
        title = data.get('title')
        recommended_anime = get_recommendations(title)
        return recommended_anime
    
api.add_resource(Anime,'/api/anime/')

if __name__ == '__main__':
    app.run(debug = True)