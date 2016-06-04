import re
import requests
from bs4 import BeautifulSoup

"""
서울대학교 생협의 메뉴를 읽어오는 코드
"""
addr1 = "https://www.snuco.com/html/restaurant/restaurant_menu1.asp" # 직영식당
addr2 = "https://www.snuco.com/html/restaurant/restaurant_menu2.asp" # 위탁식당



class snuMenu():
    map1 = { # 직영식당 매핑
            "학관":"학생회관식당", "학생회관":"학생회관식당", "학생회관식당":"학생회관식당",
            "제3식당":"제3식당", "농식":"제3식당", "농대식당":"제3식당", 
            "긱식":"기숙사식당", "기숙사":"기숙사식당", "기숙사식당":"기숙사식당",
            "자하연식당":"자하연식당", "자하연":"자하연",
            "302동식당":"302동식당", "302":"302동식당",
            "솔밭간이식당":"솔밭간이식당", "솔밭":"솔밭간이식당",
            "동원관식당":"동원관식당", "동원관":"동원관식당",
            "감골식당":"감골식당", "감골":"감골식당"
            }
    map2 = { # 위탁식당 매핑
            "서당골":"서당골", 
            "두레미담":"두레미담", "두레":"두레미담",
            "301동식당":"301동식당", "301":"301동식당",
            "예술계식당":"예술계식당", "예술계":"예술계식당", "예술":"예술계식당",
            "공대간이식당":"공대간이식당", "공깡":"공대간이식당", "공간":"공대간이식당",
            "상아회관":"상아회관", "상아":"상아회관",
            "220동식당":"220동식당", "220":"220동식당"
            }       

    soup1 = None
    soup2 = None
    map_req = {     # 식당 소속에 따른 크롤링 매핑
            1:requests.get(addr1, verify=False), 2:requests.get(addr2, verify=False), 3:None
            }
    map_soup = {    # 식당 소속에 따른 코드 추출 결과 매핑
            1:soup1, 2:soup2
            }
    map_index = {  # 직영식당의 식당명에 따른 번호 매핑
            "학생회관식당":1, "제3식당":2, "기숙사식당":3, "자하연식당":4, 
            "302동식당":5, "솔밭간이식당":6, "동원관식당":7, "감골식당":8,
                    # 위탁식당의 식당명에 따른 번호 매핑
            "서당골":1, "두레미담":2, "301동식당":3,
            "예술계식당":4, "공대간이식당":5, "상아회관":6, "220동식당":7
            }

    map_price = {   # 가격 매핑
            'ⓐ':"2500원", 'ⓑ':"3000원", 'ⓒ':"3500원",
            'ⓓ':"4000원", 'ⓔ':"4500원", 'ⓕ':"5000원", 'ⓖ':" 기타"}

    def __init__(self, string):
        # instance에 고유한 변수들을 생성한다
        self.name = None        # [식당명]
        self.belong = 1         # [직영 1/위탁 2/잘못된 식당]
        self.time = None        # [아침/점심/저녁]

        # 입력시 받은 문구를 [식당명]과 [아침/점심/저녁]으로 parsing한다.
        token = string.split()
        length = len(token)
        
        if length != 1 and length != 2:
            self.belong = 3
            return

        
        # 식당명과 소속 구하기
        self.name = snuMenu.map1.get(token[0], None)
        if not self.name:
            self.name = snuMenu.map2.get(token[0], None)
            self.belong = 2          # 위탁식당 소속
        if not self.name:
            self.name = token[0]
            self.belong = 3          # 잘못된 식당명
   
        if length == 2:
            # 인자가 두개 들어온 경우 [아침/점심/저녁] 인지 확인한다
            # 올바르지 않은 경우, None으로 두고 아침/점심/저녁 메뉴를 모두 출력하게 한다
            if token[1] == "아침" or token[1] == "점심" or token[1] == "저녁":
                self.time = token[1]

        snuMenu.update(self.belong)


    def update(num):
        # 식단 정보 업데이트
        req = snuMenu.map_req[num]
        req.encoding = "euc-kr"
        s_raw = BeautifulSoup(req.text, "html.parser")
        s_raw = s_raw.find_all('tbody')
        soup = s_raw[3].find_all("tr")
        snuMenu.map_soup[num] = soup


    def getMenu(self):
        # 해당 식당의 아침, 점심, 저녁 메뉴를 읽어들인다
        if self.belong == 3:
            # 잘못된 명령어
            return "잘못된 식당 이름입니다"
        
        result = '<'+ self.name + '> '
        index = snuMenu.map_index[self.name]
        soup_all = snuMenu.map_soup[self.belong][index]
        soup = soup_all.find_all("td")
        if self.time == "아침":
            result += "아침: " + snuMenu.prettify(soup[2].text)
        elif self.time == "점심":
            result += "점심: " + snuMenu.prettify(soup[4].text)
        elif self.time == "저녁":
            result += "저녁: " + snuMenu.prettify(soup[6].text)
        else:
            result += ( "아침: " + snuMenu.prettify(soup[2].text)  
                        + "\n점심: " + snuMenu.prettify(soup[4].text) 
                        + "\n저녁: " + snuMenu.prettify(soup[6].text)
                        )
            
        return result

    def prettify(string):
        # 가격 정보를 넣어준다 ex. 치킨텐더(3000원)
        # 채식 정보도 같이 넣어준다 ex. 연두부비빔밥[채식](3500원)
        # 아무 정보 없는 경우를 처리한다 ex. 없음
    
        string = string.strip()
        if not string:
            return "없음"

        parsed = re.split(" |\n|/", string)   # space와 개행문자로 split한다
        
        output_list = list(map( 
                        (lambda s: 
                            s[1:].replace("(*)", "[채식]")+'('+snuMenu.map_price[s[0]]+')'),
                        parsed)
                        ) 
        output = ""
        for o in output_list:
            output += o + " "
        return output
