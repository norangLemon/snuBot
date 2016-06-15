from flask import Flask, render_template
from db import *
app = Flask(__name__)

@app.route('/')
def ranking():
    keyList = r.keys("*")
    resultList = []
    for item in keyList:
        name = r.hget(item, "name").decode('utf-8')
        cmd = int(r.hget(item, "cmd"))
        chat = int(r.hget(item, "chat"))
        score = cmd + chat

        resultItem = {'name':name, 'score':score}
        resultList.append(resultItem)

    resultList = sorted(resultList, key = lambda dic: dic['score'], reverse = True)

    return render_template('ranking.html', resultList=resultList)


