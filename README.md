snu bot [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
---------
telegram bot in python

### version

#### Language

* python 3.5.1
    * [async. IO python docs.](https://www.python.org/dev/peps/pep-0492/)

#### Database & Driver

* [redis 2.4.10](http://redis.io/): open source (BSD licensed), in-memory data structure store, used as database, cache and message broker 
* [python redis 2.10.5](https://redislabs.com/python-redis): enable running Redis datasets in a highly available and auto-scalable manner, with predictable top performance

#### Webserver

* [nginx 1.8.1](http://nginx.org/): HTTP and reverse proxy server, a mail proxy server, and a generic TCP/UDP proxy server

#### Library

* [telepot 8.1](https://github.com/nickoala/telepot): Python framework for Telegram Bot API
* [requests 2.10.0](http://docs.python-requests.org/en/master/): HTTP library for Python
* [beautiful soup 4.4.1](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Python library for pulling data out of HTML and XML files
* [flask 0.11.1](http://flask.pocoo.org/docs/0.11/): webdevelopment framework for Python
* [Jinja2 2.8](http://jinja.pocoo.org/): a full featured template engine for Python

#### Clone

* [python calculator](https://github.com/xdoju/Delphox/blob/master/arith.py): Python calculator for string input


### feature

#### [날씨](https://github.com/norangLemon/naverWeather/blob/master/README.md)

* [네이버 날씨](http://weather.naver.com/)의 도시별 날씨를 검색한다.
* `/날씨 [도시명]`으로 검색하면 오늘, 내일의 오전/오후 날씨를 출력한다. 도시명을 넣지 않으면 서울 날씨를 출력한다.
* 예시: `/날씨` 명령을 한 결과

```
[서울 날씨 검색 결과]
- 오늘(6.07.)
오전: 19.0℃(흐림, 강수확률 30%)
오후: 26.0℃(구름많음, 강수확률 20%)
- 내일(6.08.)
오전: 18.0℃(구름많음, 강수확률 20%)
오후: 28.0℃(구름조금, 강수확률 10%)
```

#### [메뉴](https://github.com/norangLemon/snuMenu)

* [직영식당](https://www.snuco.com/html/restaurant/restaurant_menu1.asp), [위탁식당](https://www.snuco.com/html/restaurant/restaurant_menu2.asp)의 오늘 메뉴를 알려준다.
* `/[식단, 메뉴] [식당명] [아침, 점심, 저녁]`을 입력하면 해당 식당의 해당 시간 메뉴를 보여준다. 시간을 입력하지 않으면 전체 시간 메뉴를 불러온다.
* 예시: `/메뉴 학관 점심` 명령 결과

```
<학생회관식당> 점심: 치킨마요덮밥(4000원) 참치채소죽(2500원) 부대찌개(4000원) 바지락칼국수(4000원) 마파두부덮밥(3500원)
```

#### 계산기

* [계산기](https://github.com/xdoju/Delphox/blob/master/arith.py)를 사용해서 수식을 계산한다.
* `/계산 [수식]`을 입력하면 수식의 계산값을 출력한다.
* 예시: `/계산 300/3+2*(5-2)` 명령 결과

```
106.0
```

#### 사전

* [다음 사전](http://dic.daum.net/)의 단어 검색 결과를 출력한다.
* `/[사전, 국어, 영어, 일어] [검색어]`를 입력하면 `[사전명] 표제어: 뜻`의 형식으로 결과를 출력한다.
* 예시: `/사전 샤샤`

```
[중국어] 沙沙: 사박사박, 쏴쏴, 삭삭, 모래
```

#### 심심이

* 인사를 하면 받아준다
* 말하는 문장 중에 참치가 포함되어있으면, 참치를 달라고 한다.

#### Web Page

Web Page를 서버에서 실행할 경우, 랭킹을 확인 가능하다.

* 랭킹, 이름, 점수를 띄어줌
* 명령어 실행 횟수에 따라서 점수 증가
* 심심이 기능을 사용함에 따라서 점수가 증감
* telegram상 이름을 바꾸면 바로 반영

