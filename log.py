import logging
import logging.handlers
import sys

# log file 만들기
# '/'로 시작하는 command와 샤샤의 심심이 기능을 분리해서 로그를 남긴다
# 일반 채팅은 로그를 남기지 않는다

# 최상위 loger에게 stdout으로 출력하도록 한다
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s|%(name)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

# child logger는 file에 출력한다
# command log용 hander 생성
cmd_logger = logging.getLogger('cmdLoger')
cmd_fileHandler = logging.FileHandler('Logs/command.log') 
cmd_streamHandler = logging.StreamHandler()

# 심심이 log용 handler 생성
chat_logger = logging.getLogger('chatLoger')
chat_fileHandler = logging.FileHandler('Logs/chat.log') 
chat_streamHandler = logging.StreamHandler()

# 동등한 파일 형식 사용

#     [파일명: 줄번호] <레벨>
# 메시지
formatter = logging.Formatter('\t[%(filename)s: %(lineno)s] <%(levelname)s> %(asctime)s\n%(message)s')

# 형식 적용, 핸들러를 로거에 추가, 레벨 설정
chat_fileHandler.setFormatter(formatter)
cmd_fileHandler.setFormatter(formatter)

chat_logger.addHandler(chat_fileHandler)
cmd_logger.addHandler(cmd_fileHandler)

chat_logger.addHandler(chat_streamHandler)
chat_logger.addHandler(cmd_streamHandler)

cmd_logger.setLevel(logging.DEBUG)
chat_logger.setLevel(logging.DEBUG)

# 함수명 alias
cmd_prtErr = cmd_logger.error
cmd_prtLog = cmd_logger.debug

chat_prtErr = chat_logger.error
chat_prtLog = chat_logger.debug
