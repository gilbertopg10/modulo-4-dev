from flask import Flask, jsonify
from pymongo import MongoClient
import json

api = Flask(__name__)

@api.route('/')
def welcome():
    return "Bienvenido a la API Video Charts"

# Conexión a la base de datos MongoDB
url = "mongodb+srv://gilbertoparragaxiola:pruzKKQrfsr5oQ4W@clusterpy.wvlrzui.mongodb.net/"
cliente = MongoClient(url)
db = cliente["Most_Popular_Videos"]

# Muestra los registros según la región del parametro, lista_de_regiones = ["US", "CA", "GB", "AU", "DE", "FR", "JP", "KR", "BR", "MX"]
@api.route('/videos/<string:region_code>', methods=['GET'])
def get_videos_by_region(region_code):
    coll_name = region_code.lower()
    coll = db[coll_name]
    
    videos = []
    for video in coll.find():
        videos.append(json.loads(json.dumps(video, default=str)))  # Convertir ObjectId a str
    
    return jsonify(videos)

#obtiene el video con más vistas de cada región

@api.route('/top_videos', methods=['GET'])
def get_top_videos():
    top_videos = []
    collections = ["us", "ca", "gb", "au", "de", "fr", "jp", "kr", "br", "mx"]

    for collection in collections:
        coll = db[collection]
        top_video = coll.find_one(sort=[("statistics.viewCount", -1)])
        if top_video:
            top_videos.append(json.loads(json.dumps(top_video, default=str)))

    return jsonify(top_videos)


if __name__ == '__main__':
    api.run(debug=True, host="localhost", port=5002)

