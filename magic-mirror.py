#! usr/bin/python
# coding=utf-8
from flask import Flask, render_template, jsonify, request
import task
import random
import mirrorutil as util
from  httplib2 import Http
from voices import Voice2Text
import  json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html", city="成都", r=random.uniform(1, 20))


@app.route('/weather')
def weather():
    http = Http()
    url = 'https://api.thinkpage.cn/v3/weather/daily.json?key=kmeoh6g3el2xlpun&location={0}&language=zh-Hans&unit=c&start=0&days=5?r={1}'.format(util.Config.city["cityName"],
                                                                                   random.uniform(1, 20))
    headers = {'Content-type': 'application/json; charset=utf-8'}
    response, content = http.request(url, "GET", headers=headers)
    str = content.decode("utf-8")
    return jsonify(json.loads(str));

@app.route('/weather/now')
def weather_now():
    http = Http()
    url = 'https://api.thinkpage.cn/v3/weather/now.json?key=kmeoh6g3el2xlpun&location={0}&language=zh-Hans&unit=c?r={1}'.format(util.Config.city["cityName"],
                                                                                   random.uniform(1, 20))
    headers = {'Content-type': 'application/json; charset=utf-8'}
    response, content = http.request(url, "GET", headers=headers)
    str = content.decode("utf-8")
    return jsonify(json.loads(str));
@app.route('/config', methods=['GET'])
def config():
    return jsonify(util.Config.get_dconfig())


if __name__ == '__main__':
    task.Task().start()
    app.jinja_env.variable_start_string = "[["
    app.jinja_env.variable_end_string = "]]"
    app.run()
