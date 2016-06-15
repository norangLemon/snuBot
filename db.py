# id, name, cmd, chat -> score
import redis

r = redis.Redis('localhost')
dbKeyPrefix = "shasha-userinfo-"

def getDBKey(id):
    return dbKeyPrefix + str(id)

def pushDB(id, name):
    dbKey = getDBKey(id)
    r.hset(dbKey, 'name', name)
    r.hset(dbKey, 'cmd', "0")
    r.hset(dbKey, 'chat', '0')

def cmdPlus(id, name):
    dbKey = getDBKey(id)

    if not r.exists(dbKey):
        pushDB(id, name)

    if(r.hget(dbKey, 'name') != name):
        r.hset(dbKey, 'name', name)
    cmdValue = int(r.hget(dbKey, 'cmd')) + 1
    r.hset(dbKey, 'cmd', str(cmdValue))

