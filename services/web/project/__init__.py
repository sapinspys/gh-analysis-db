import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource, abort
from .functions import *

app = Flask(__name__)
CORS(app)
api = Api(app)

def abort_if_not_authorized():
    token = request.headers['Authorization']
    if token:
        return token
    else:
        abort(404, message="Authorization header missing.")


class Index(Resource):
    def get(self):
        return {"message": "Server running OK."}


class RepoSummary(Resource):
    def get(self, owner, repo):
        token = abort_if_not_authorized()
        data = repository_summary(token, f'{owner}/{repo}')
        return data


class Top10Contributors(Resource):
    def get(self, owner, repo):
        token = abort_if_not_authorized()
        data = top_contributors(token, f'{owner}/{repo}')
        return data


class YearlyCommitActivity(Resource):
    def get(self, owner, repo):
        token = abort_if_not_authorized()
        data = yearly_commit_activity(token, f'{owner}/{repo}')
        return data


class YearlyCodeFrequency(Resource):
    def get(self, owner, repo):
        token = abort_if_not_authorized()
        data = yearly_code_frequency(token, f'{owner}/{repo}')
        return data


api.add_resource(Index, '/')
api.add_resource(RepoSummary, '/repo-summary/<owner>/<repo>')
api.add_resource(Top10Contributors, '/visualization/top-10-contributors/<owner>/<repo>')
api.add_resource(YearlyCommitActivity, '/visualization/yearly-commit-activity/<owner>/<repo>')
api.add_resource(YearlyCodeFrequency, '/visualization/yearly-commit-activity/<owner>/<repo>')


if __name__ == '__main__':
    DEBUG = bool(os.environ.get('DEBUG'))
    app.run(debug=DEBUG)
