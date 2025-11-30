from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    # Find the picture with the matching ID
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    # If no picture found with that ID
    return {"message": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Get JSON data from request
    picture_data = request.get_json()
    
    # Check if picture with this ID already exists
    for picture in data:
        if picture["id"] == picture_data["id"]:
            return {"Message": f"picture with id {picture_data['id']} already present"}, 302
    
    # Add new picture to data
    data.append(picture_data)
    return jsonify(picture_data), 201

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Get JSON data from request
    picture_data = request.get_json()
    
    # Find and update the picture with matching ID
    for i, picture in enumerate(data):
        if picture["id"] == id:
            data[i] = picture_data
            return jsonify(picture_data), 200
    
    # If no picture found with that ID
    return {"message": "Picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find and remove the picture with matching ID
    for i, picture in enumerate(data):
        if picture["id"] == id:
            deleted_picture = data.pop(i)
            return jsonify(deleted_picture), 204
    
    # If no picture found with that ID
    return {"message": "Picture not found"}, 404