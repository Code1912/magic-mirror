#! usr/bin/python
# coding=utf-8
from flask import Flask, render_template, jsonify, request
import task
import random
import mirrorutil as util
from voices import Voice2Text

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html", city="成都", r=random.uniform(1, 20))


@app.route('/config', methods=['GET'])
def config():
    return jsonify(util.Config.get_dconfig())


@app.route('/voice2text', methods=['POST'])
def vocice2text():
    if request.method != 'POST':
        return ""
    size = request.json['size']
    base64 = request.json['base64']
    return jsonify(Voice2Text.voice2text(size, base64))


if __name__ == '__main__':
    task.Task().start()
    app.jinja_env.variable_start_string = "[["
    app.jinja_env.variable_end_string = "]]"
    app.run()
