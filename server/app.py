#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        get_plant = Plant.query.all()
        plants_dict = [plant.serialize() for plant in get_plant]
        response = make_response(jsonify(plants_dict),200)
        return response
    
    def post(self):
        data = request.get_json()

        name = data.get("name")
        image = data.get("image")
        price = data.get("price")

        new_data = Plant(name = name,image=image,price = price)
        db.session.add(new_data)
        db.session.commit()

        response = make_response(jsonify(new_data.serialize()),200)
        return response
api.add_resource(Plants, "/plants")




class PlantByID(Resource):
    def get(self,id):
        get_id = Plant.query.get(id)
        if not get_id:
            return {"error": "not found"}
        else:
            plant_dict =  get_id.serialize()
            response = make_response(jsonify(plant_dict),200)
            return response

api.add_resource(PlantByID, "/plants/<int:id>")
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
