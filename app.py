from flask import Flask, jsonify, request, render_template
from models import Region, Category, VoteResult
from settings import app, db

# Terminal instructions:
# . web-tech/bin/activate
# export FLASK_APP=app.py
# export FLASK_DEBUG=1
# python parse_csv.py btw17_kerg.csv
# flask run

@app.route("/", methods=["GET"])
def login():
    return render_template('index.html')

# region actions

@app.route("/region/<int:id>", methods=["GET"])
def getRegion(id):
    if id:
        region = Region.query.get(id)
        if region:
            return jsonify(region.as_dict()), 200

@app.route("/region/<int:id>/constituencies", methods=["GET"])
def getConstituenciesOfRegion(id):
    if id:
        region = Region.query.get(id)
        if region:
            output = []
            for constituency in region.constituencies:
                output.append(constituency.as_dict())

            return jsonify(output), 200

@app.route("/region/<int:id>/voteResults", methods=["GET"])
def getVoteResultsOfRegion(id):
    if id:
        region = Region.query.get(id)
        if region:
            output = []
            for voteResult in region.voteResults:
                output.append(voteResult.as_dict())

            return jsonify(output), 200

@app.route("/region/<int:id>/state", methods=["GET"])
def getStateOfRegion(id):
    if id:
        region = Region.query.get(id)
        if region and region.state:
            return jsonify(region.state.as_dict()), 200

@app.route("/states", methods=["GET"])
def getStates():
    output = []
    regions = Region.query.filter(Region.state == None).all()
    for region in regions:
        output.append(region.as_dict())

    return jsonify(output), 200

# category actions

@app.route("/category/<int:id>", methods=["GET"])
def getCategory(id):
    if id:
        category = Category.query.get(id)
        if category:
            return jsonify(category.as_dict()), 200

@app.route("/category/<int:id>/voteResults", methods=["GET"])
def getVoteResultsOfCategory(id):
    if id:
        category = Category.query.get(id)
        if category:
            output = []
            for voteResult in category.voteResults:
                output.append(voteResult.as_dict())

            return jsonify(output), 200

# voteResult actions

@app.route("/voteResult/<int:id>", methods=["GET"])
def getVoteResult(id):
    if id:
        voteResult = VoteResult.query.get(id)
        if voteResult:
            return jsonify(voteResult.as_dict()), 200

@app.route("/voteResult/<int:id>/region", methods=["GET"])
def getRegionOfVoteResult(id):
    if id:
        voteResult = VoteResult.query.get(id)
        if voteResult and voteResult.region:
            return jsonify(voteResult.region.as_dict()), 200

@app.route("/voteResult/<int:id>/category", methods=["GET"])
def getCategoryOfVoteResult(id):
    if id:
        voteResult = VoteResult.query.get(id)
        if voteResult and voteResult.category:
            return jsonify(voteResult.category.as_dict()), 200
