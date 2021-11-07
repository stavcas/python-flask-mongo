#!/usr/bin/env python3
from flask import Flask, jsonify, request
from werkzeug.wrappers import response
import pymongo

mongo_client = pymongo.MongoClient("mongodb://db:27017/")

mydb = mongo_client['main']
mycol = mydb['names']

app = Flask(__name__)

username = "You"


def save_name_to_db(name):
    global mycol
    mycol.update_one({}, {'$set': {"name": name}}, upsert=True)


def read_name_from_db():
    global mycol
    result = mycol.find_one()

    if result is None:
        result = "Stranger"
    print(result)

    return result["name"]


@app.route('/hello')
def say_hello():
    username = read_name_from_db()
    return "Hello, " + username


@app.route('/hello', methods=['POST'])
def say_hello_to_user():
    current_name = request.get_data(as_text=True)
    return "hello " + current_name, 200


@app.route('/hello', methods=['PUT'])
def update_user_name():
    username = request.get_data(as_text=True)
    save_name_to_db(username)
    return '', 204
