#!/usr/bin/env python3
from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Production, CrewMember

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Productions(Resource):

    def get(self):
        production_list = [prod.to_dict() for prod in Production.query.all()]
        response = make_response(
            production_list,
            200,
        )
        return response

    def post(self):
        new_production = Production(
            **request.json
        )

        db.session.add(new_production)
        db.session.commit()
        response = new_production.to_dict()

        return make_response(
            response,
            201,
        )
    

class ProductionById(Resource):

    def get(self, id):
        production = Production.query.filter_by(id=id).first().to_dict()
        return make_response(production, 200)

    def delete(self, id):
        production = Production.query.filter_by(id=id).first()
        db.session.delete(production)
        db.session.commit()

        return make_response('', 204)

    def patch(self, id):
        production = Production.query.filter_by(id=id).first()
        for key in request.json:
            setattr(production, key, request.json[key])
        db.session.add(production)
        db.session.commit()

        return make_response(
            production.to_dict(),
            200
        )

api.add_resource(Productions, '/productions') # get, post
api.add_resource(ProductionById, '/productions/<int:id>') # get, delete, patch

