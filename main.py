import setting, words
import sys, signal
import asyncio
import random
import telepot
import telepot.async
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

from snuMenu import *
from daumDic import *
from naverWeather import *
from log import *
import arith
"""
skeleton from https://github.com/nickoala/telepot/blob/master/examples/skeletona_route.py
"""

message_with_inline_keyboard = None
inline_chat_id = None

async def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    cmd_prtLog('Chat:%s %s %s' %(content_type, chat_type, chat_id))
    global inline_chat_id
    global message_with_inline_keyboard
    
    if content_type == 'new_chat_member':
            # 새로운 멤버가 들어왔거나, 봇이 새로운 곳에 초대된 경우
            cmd_prtLog("new_chat_memeber: %s"  %chat_id)
            await bot.sendMessage(chat_id, words.greet)
            return
        
    elif content_type != 'text':
        return
    input_msg = msg['text']
    commands = input_msg.split()
    command = commands[0]
    if command[0] == '/' and len(command) >= 3:
        # '/'로 시작하는 경우 명령어로 간주한다
        # 길이가 3보다 짧으면 명령어가 아니다
        cmd_prtLog("new_chat_memeber: %s"  %chat_id)
        
        if command in ["/도움", "/help", "/도움말", "/start"]:
            await bot.sendMessage(chat_id, words.help)
        
        elif command in ["/식단", "/메뉴"]:
            menu = snuMenu(input_msg[4:])
            await bot.sendMessage(chat_id, menu.getMenu())
        
        elif command[1:] in daumDic.map_dic.keys():
            search = daumDic(input_msg[1:])
            await bot.sendMessage(chat_id, search.getResult())

        elif command == "/계산":
            result = arith.calculate(input_msg[4:])
            await bot.sendMessage(chat_id, result)

        elif command == "/날씨":
            weather = naverWeather(input_msg[4:])
            await bot.sendMessage(chat_id, weather.getWeather())

    # 심심이 기능
    elif input_msg in ["샤샤야 안녕!", "샤샤 안녕!", "샤샤 안녕?", "샤샤야 안녕?", "안녕!", "안녕?", "안녕"]:
        # 인사 받아주기
        await bot.sendMessage(chat_id, words.hi())

 
    elif input_msg.find("참치") != -1:
        # 참치 달라고 하기
        print("참치")
        markup = InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text=words.giveTuna(), callback_data='give tuna')],
                     [InlineKeyboardButton(text=words.notGiveTuna(), callback_data='not give tuna')],
                 ])

        inline_chat_id = chat_id

        message_with_inline_keyboard = await bot.sendMessage(chat_id, words.heardTuna(), reply_markup=markup)
    
    elif input_msg == "test":
        # 선택지 추가 테스트
        print("test")
        markup = InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text="A", callback_data='A')],
                     [InlineKeyboardButton(text="B", callback_data='B')],
                 ])

        inline_chat_id = chat_id

        message_with_inline_keyboard = await bot.sendMessage(chat_id, words.heardTuna(), reply_markup=markup)

def on_inline_query(msg):
    # 인라인 쿼리는 쓰지 않음
    def compute():
        return "I do nothing!XD"
    answerer.answer(msg, compute)

async def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    
    global inline_chat_id
    if data == 'give tuna':         # 참치를 주면 기뻐하기
        await bot.answerCallbackQuery(query_id, text='참치를 주었다!')
        await bot.sendMessage(inline_chat_id, words.thx())
    elif data == 'not give tuna':   # 참치를 안 주면 슬퍼하기
        await bot.answerCallbackQuery(query_id, text='참치를 주지 않았다!')
        await bot.sendMessage(inline_chat_id, words.sad())

    elif data == 'A':
        await bot.sendMessage(inline_chat_id, "A")
    elif data == 'B':
        await bot.sendMessage(inline_chat_id, "B")

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)


TOKEN = setting.token 

bot = telepot.async.Bot(TOKEN)
answerer = telepot.async.helper.Answerer(bot)

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop({'chat': on_chat_message,
                                   'callback_query': on_callback_query,
                                   'inline_query': on_inline_query,
                                   'chosen_inline_result': on_chosen_inline_result}))

# ^C로 끌 때 에러메시지 나오지 않게 하기
def signal_handler(signal, frame):
    print('Bye!')
    exit(0)
signal.signal(signal.SIGINT, signal_handler)


print('ShaShaBot is on its way!')
loop.run_forever()
