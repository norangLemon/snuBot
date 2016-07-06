from flask import Flask, render_template
from db import *
app = Flask(__name__)


@app.route('/rank') # rank page에서 띄우도록 한다.
def ranking():
    keyList = r.keys("*")
    resultList = []
    for item in keyList:
        name = r.hget(item, "name").decode('utf-8')
        # 디비에서 이름을 읽어오고, byte 타입을 string으로 전환해줌
        cmd = int(r.hget(item, "cmd"))
        chat = int(r.hget(item, "chat"))
        score = cmd + chat
        # 순위 계산은 단순히 명령어 실행 횟수와 심심이 기능으로 얻은 점수의 합으로 한다.

        resultItem = {'name':name, 'score':score}
        resultList.append(resultItem)
        # 결과는 딕셔너리의 리스트로 하여서 정렬과 웹 페이지 띄우기에 좋게 한다.

    resultList = sorted(resultList, key = lambda dic: dic['score'], reverse = True)
    # score에 따라서 오름차순 정렬한다

    return render_template('ranking.html', resultList=resultList)
    # 화면을 띄우게 한다.

