import base64
import calendar
import time

from flask import Flask, request
from flask.json import jsonify

from utils.DBHandler import DBHandler

app = Flask(__name__)

IMAGE_BASE_PATH = "static/images/"


def get_success_response(message=None, data=None):
    response = {'error': 0, 'message': message, 'response': data}
    return jsonify(response)


def get_error_response(message):
    response = {'error': 1, 'message': message}
    return jsonify(response)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/register', methods=['POST'])
def register():
    user = request.json
    login_id = DBHandler.register(user)
    if login_id == -1:
        return get_error_response("username exists")
    return get_success_response("success", login_id)


@app.route('/login', methods=['POST'])
def login():
    user = request.json
    user = DBHandler.login(user)
    if user:
        return get_success_response("success", user[0])
    return get_error_response("login failed")


@app.route('/recipe/_save', methods=['POST'])
def save_recipe():
    recipe = request.json
    image_data = recipe['image']

    ts = calendar.timegm(time.gmtime())

    file_name = IMAGE_BASE_PATH + "recipe_" + str(ts) + ".jpg"
    with open(file_name, "wb") as fh:
        fh.write(base64.b64decode(image_data))

    recipe['image'] = file_name

    recipeId = DBHandler.save_recipe(recipe)
    if recipeId:
        return get_success_response("success", recipeId)
    return get_error_response("login failed")


@app.route('/recipe/_update', methods=['POST'])
def update_recipe():
    recipe = request.json
    image_data = recipe['image']

    ts = calendar.timegm(time.gmtime())

    file_name = IMAGE_BASE_PATH + "recipe_" + str(ts) + ".jpg"
    with open(file_name, "wb") as fh:
        fh.write(base64.b64decode(image_data))

    recipe['image'] = file_name

    recipeId = DBHandler.update_recipe(recipe)
    if recipeId:
        return get_success_response("success", recipeId)
    return get_error_response("login failed")


@app.route('/recipe/_delete', methods=['POST'])
def delete_recipe():
    recipeId = request.args.get("recipeId")
    DBHandler.get_recipe(recipeId)
    return get_success_response("success")


@app.route('/recipe/_get', methods=['GET'])
def get_recipe():
    category = request.args.get("category")
    result = DBHandler.get_recipe(category)
    return get_success_response("success", result)


@app.route('/comment/_save', methods=['POST'])
def add_comment():
    comment = request.json
    commentId = DBHandler.add_comment(comment)
    return get_success_response("success", commentId)


@app.route('/comment/_get', methods=['POST'])
def get_comment():
    recipeId = request.args.get("recipeId")
    comments = DBHandler.get_comment(recipeId)
    return get_success_response("success", comments)


@app.route('/feedback/_save', methods=['POST'])
def save_feedback():
    feedback = request.json
    feedbackId = DBHandler.save_feedback(feedback)
    return get_success_response("success", feedbackId)


@app.route('/feedback/_get', methods=['POST'])
def get_feedback():
    feedback = DBHandler.get_feedback()
    return get_success_response("success", feedback)


@app.route('/recipe/_search', methods=['GET', 'POST'])
def searchRecipe():
    ingredients = request.json
    recipe = DBHandler.search_recipe(ingredients)
    return get_success_response("success", recipe)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
