import random

help = """냐옹! 
서울대생을 위한 고양이 샤샤다냥! >ㅅ<
샤샤한테 일을 시키려면 맨 앞에 '/'를 붙여달라냥!
http://telegram.norang.xyz 에서 샤샤와의 친밀도를 확인할 수 있다냥~

/날씨 [지역]: [지역]의 날씨를 불러온다냥! 
'/날씨'만 하면 서울의 날씨를 불러온다냥!
ex. /날씨 고양

/계산 [수식]: [수식]을 계산한다냥! 
너무 복잡한 계산은 잘 못한다냥! ㅠㅠ
ex. /계산 (3+4)/7

/[사전, 국어, 영어, 일어] [검색어]: [검색어]를 사전에서 찾는다냥! 
ex. /영어 shasha

/[메뉴, 식단] [식당명] [아침, 점심, 저녁]: [식당명]의 오늘 메뉴를 알려준다냥!
시간을 정하지 않으면 오늘의 메뉴를 전부 보여준다냥~
ex. /식단 학관

/[도움, help]: 지금 보고 있는 도움말을 다시 보여준다냥~
ex. /help"""

greet = """반갑다냥!>ㅅ<
나는 고양이 샤샤다냥!
내가 뭘 하는 봇인지 궁금해요냥?
'/도움'을 입력해보라냥! X3"""

def hi():
    l = ["안냥!>ㅅ<","안녕하세요XD", "안녕하세요냥!+ㅅ+", "와아앙! 인사해주셔따!*ㅅ* 샤샤는 안녕해요냥!", "안녕하다요냥~ >ㅅ<"]
    return random.choice(l)

def heardTuna():
    l = ["참치!! 참치 소리를 들었다냥!", "우웅?? 참치?!", "냐앙? 샤샤가 좋아하는 참치!"]
    return random.choice(l)

l_giveTuna = ["참치 줄게!", "참치 먹으렴ㅎㅎ", "여기 참치 먹자~"]
def giveTuna():
    return random.choice(l_giveTuna)

l_notGiveTuna = ["참치 안 줄건데?", "너 줄 거 아닌데?", "참치가 어디있다고 그래?"]
def notGiveTuna():
    return random.choice(l_notGiveTuna)

def thx():
    l = ["와아아!! 고맙다냥>ㅅ<", "와옹! 참치! 챱챱0ㅅ0", "참치다!XD"]
    return random.choice(l)

def sad():
    l = ["시무룩...", "후애앵8ㅅ8", "(˃̣̣̣̣̣̣ㅅ˂̣̣̣̣̣̣ ू)"]
    return random.choice(l)
