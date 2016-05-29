"""
Views
"""
from utils import err, get_post_data
from models import db, Article, Citations

from flask import request, current_app
from flask.ext.restful import Resource


class SentimentView(Resource):
    """
    End point for sentinments
    """
    def get():
        return {'sentiment': 0}, 200

