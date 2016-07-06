import re
import requests
from bs4 import BeautifulSoup

# daum 어학사전을 검색
# http://dic.daum.net/

class daumDic():
    addr = "http://dic.daum.net/search.do?q="
    addr_re = "http://dic.daum.net/word/view.do?wordid="    # 리다이렉트 되는 경우가 있음
    map_dic = {     # 사전 조건 매핑
            "사전":"",
            "국어":"&dic=kor",
            "영어":"&dic=eng",
            "일어":"&dic=jp"
            }

    def __init__(self, string):
        # instance 변수 설정
        ## 검색 키워드
        self.word = None 
        self.dic = None
        ## BeautifulSoup 파싱: 검색 결과
        self.search_word = None
        self.search_list = None
        self.search_dic = None
        ## 출력할 검색 결과

        # 명령어 parsing
        parsed = string.split()

        if len(parsed) != 2:
            return
        
        self.dic = daumDic.map_dic.get(parsed[0])
        self.search_dic = parsed[0]
        self.word = parsed[1]

        self.search()

    def search(self):
        if not self.word:
            return ""
        addr = daumDic.addr + self.word + self.dic
        
        req = requests.get(addr)
        req.encoding = "utf-8"

        soup_raw = BeautifulSoup(req.text, "html.parser")
        print(soup_raw)
        
        # 특정 검색의 경우, js를 사용하여 redirect 되기도 한다.
        # 이때는 단어의 번호(word_key)를 코드에서 찾아낼 수 있다.
        # 이것을 이용하여 특정한 경우에는 주소를 다시 바꾸어 크롤링한다.
        word_key = re.compile("((kew)|(ekw))\d{9}").search(soup_raw.text)                 # 매칭되는 케이스가 있는지 검색한다
        if word_key:
            print(word_key)
            addr = daumDic.addr_re + word_key.group() + "&q=" + self.word       # 검색 결과로 redirect되는 주소를 알아낸다
            req = requests.get(addr)
            soup_raw = BeautifulSoup(req.text, "html.parser")
        
        self.search_word = soup_raw.find(class_= re.compile("txt_clean"))
        if not self.search_word:
            # 검색에 실패한 경우
            return

        if self.search_dic == "사전":
            self.search_dic = soup_raw.find("h4", class_="tit_word").text.strip('사전')

        soup = soup_raw.find(class_="search_box")
        
        if not soup:
            # 페이지 형식이 다른 경우
            soup = soup_raw.find(class_="inner_top")

            # 검색 결과가 없는 경우
            if not soup:
                return
            self.search_list = soup.find(class_="list_mean").find_all(class_="txt_mean")
            
        else:    
            self.search_list = soup.find(class_="list_search").find_all(class_="txt_search")
        


    def getResult(self):
        if not self.word:
            return "검색할 단어를 입력해달라냥!\n '/사전 고양이'처럼 검색하면 된다냥!"
        if not self.search_list or not self.search_word:
            return "우웅? 그런 단어는 사전에 없다냥!"
        result = '[' + self.search_dic + '] ' + self.search_word.text + ": "

        for mean in self.search_list:
            result += mean.text + ", "
        
        return result.strip(', ')
