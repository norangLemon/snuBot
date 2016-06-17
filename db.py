# id, name, cmd, chat -> score
import redis

r = redis.Redis('localhost')
dbKeyPrefix = "shasha-userinfo-"

def getDBKey(id):
    # id로 DB의 key를 만들어준다.
    result = dbKeyPrefix + str(id)
    return result

def validateKey(dbKey, name):
    # DB에 해당 id에 대한 정보가 없으면 초기화를 해 주어 유효한 키가 되도록 한다.
    if not r.exists(dbKey):
        r.hset(dbKey, 'name', name)
        r.hset(dbKey, 'cmd', "0")
        r.hset(dbKey, 'chat', '0')

def resetName(dbKey, name):
    # 유저의 이름이 바뀐 경우 유저 이름을 갱신해준다.
    if(r.hget(dbKey, 'name') != name):
        r.hset(dbKey, 'name', name)


# main.py에서 command 실행 횟수 및 애정도를 업데이트 하기 위한 함수

def cmdPlus(id, name):
    # 해당 id 유저의 cmd 실행 횟수를 1회 상승시킨다.
    dbKey = getDBKey(id)
    validateKey(dbKey, name)
    resetName(dbKey, name)

    cmdValue = int(r.hget(dbKey, 'cmd')) + 1
    r.hset(dbKey, 'cmd', str(cmdValue))

def chatPlus(id, name, num):
    # 해당 id 유저의 애정도를 num 만큼 상승시킨다
    dbKey = getDBKey(id)
    validateKey(dbKey, name)
    resetName(dbKey, name)

    chatValue = int(r.hget(dbKey, 'chat')) + num
    r.hset(dbKey, 'chat', str(chatValue))
