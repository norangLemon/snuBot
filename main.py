import setting, words
from snuMenu import *

import sys, signal

import asyncio
import random
import telepot
import telepot.async
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

"""
$ python3.5 skeletona_class.py <token>

An example that demonstrates the use of custom keyboard and inline keyboard, and their various buttons.

Before running this example, remember to `/setinline` and `/setinlinefeedback` to enable inline mode for your bot.

The bot works like this:

- First, you send it one of these 4 characters - `c`, `i`, `h`, `f` - and it replies accordingly:
    - `c` - a custom keyboard with various buttons
    - `i` - an inline keyboard with various buttons
    - `h` - hide custom keyboard
    - `f` - force reply
- Press various buttons to see their effects
- Within inline mode, what you get back depends on the **last character** of the query:
    - `a` - a list of articles
    - `p` - a list of photos
    - `b` - to see a button above the inline results to switch back to a private chat with the bot
- Play around with the bot for an afternoon ...
"""

class Bot(telepot.async.Bot):
    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self._answerer = telepot.async.helper.Answerer(self)
        self._message_with_inline_keyboard = None

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print('Chat:', content_type, chat_type, chat_id)

        if content_type == 'new_chat_member':
            # 누군가 새로 들어왔거나, 봇이 새로 초대된 상황일 때
            bot.sendMessage(chat_id, words.greet)
            return

        elif content_type != 'text':
            # 그렇지 않고, text 메시지도 아닌 경우는 그냥 끝낸다.
            return

        command = msg['text']
        
        if command == "/도움":
            bot.sendMessage(chat_id, words.help)

        if command[:3] == "/식단":
            result = snuMenu(command[3:])
            bot.sendMessage(chat_id, result.getMenu())

        if command == 'c':
            markup = ReplyKeyboardMarkup(keyboard=[
                         ['Plain text', KeyboardButton(text='Text only')],
                         [dict(text='Phone', request_contact=True), KeyboardButton(text='Location', request_location=True)],
                     ])
            await self.sendMessage(chat_id, 'Custom keyboard with various buttons', reply_markup=markup)
        elif command == 'i':
            markup = InlineKeyboardMarkup(inline_keyboard=[
                         [dict(text='Telegram URL', url='https://core.telegram.org/')],
                         [InlineKeyboardButton(text='Callback - show notification', callback_data='notification')],
                         [dict(text='Callback - show alert', callback_data='alert')],
                         [InlineKeyboardButton(text='Callback - edit message', callback_data='edit')],
                         [dict(text='Switch to using bot inline', switch_inline_query='initial query')],
                     ])

            self._message_with_inline_keyboard = await self.sendMessage(chat_id, 'Inline keyboard with various buttons', reply_markup=markup)
        elif command == 'h':
            markup = ReplyKeyboardHide()
            await self.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)
        elif command == 'f':
            markup = ForceReply()
            await self.sendMessage(chat_id, 'Force reply', reply_markup=markup)

    async def on_callback_query(self, msg):
        query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
        print('Callback query:', query_id, from_id, data)

        if data == 'notification':
            await self.answerCallbackQuery(query_id, text='Notification at top of screen')
        elif data == 'alert':
            await self.answerCallbackQuery(query_id, text='Alert!', show_alert=True)
        elif data == 'edit':
            if self._message_with_inline_keyboard:
                msgid = (from_id, self._message_with_inline_keyboard['message_id'])
                await self.editMessageText(msgid, 'NEW MESSAGE HERE!!!!!')
            else:
                await self.answerCallbackQuery(query_id, text='No previous message to edit')

    def on_inline_query(self, msg):
        def compute():
            query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
            print('Computing for: %s' % query_string)

            articles = [InlineQueryResultArticle(
                            id='abcde', title='Telegram', input_message_content=InputTextMessageContent(message_text='Telegram is a messaging app')),
                        dict(type='article',
                            id='fghij', title='Google', input_message_content=dict(message_text='Google is a search engine'))]

            photo1_url = 'https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf'
            photo2_url = 'https://www.telegram.org/img/t_logo.png'
            photos = [InlineQueryResultPhoto(
                          id='12345', photo_url=photo1_url, thumb_url=photo1_url),
                      dict(type='photo',
                          id='67890', photo_url=photo2_url, thumb_url=photo2_url)]

            result_type = query_string[-1:].lower()

            if result_type == 'a':
                return articles
            elif result_type == 'p':
                return photos
            else:
                results = articles if random.randint(0,1) else photos
                if result_type == 'b':
                    return dict(results=results, switch_pm_text='Back to Bot', switch_pm_parameter='Optional start parameter')
                else:
                    return dict(results=results)

        self._answerer.answer(msg, compute)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print('Chosen Inline Result:', result_id, from_id, query_string)


TOKEN = setting.token

bot = Bot(TOKEN)
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()

# 끝낼 때 에러메시지 띄우지 않기
def signal_handler(signal, frame):
    print('종료되었습니다.')
    exit(0)
signal.signal(signal.SIGINT, signal_handler)

