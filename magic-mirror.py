#! usr/bin/python
#coding=utf-8
from flask import Flask,render_template
import task
import sys
import random
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html",city="成都",r=random.uniform(1, 20)   )


if __name__ == '__main__':
    task.Task().start()
    app.jinja_env.variable_start_string = "[["
    app.jinja_env.variable_end_string = "]]"
    app.run()
