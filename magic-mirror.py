#! usr/bin/python
#coding=utf-8
from flask import Flask,render_template
import task
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html",city="成都" )


if __name__ == '__main__':
    task.Task().start()
    app.run()
