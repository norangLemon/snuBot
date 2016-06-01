import setting
import asyncio
import telepot
import telepot.async
from telepot.namedtuple import Message


async def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)
    if content_type == 'text':
        # text-message handling
        await bot.sendMessage(chat_id, msg['text'])

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print ('Callback Query:', query_id, from_id, query_data)

def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    print('Inline Query:', query_id, from_id, query_string)

    def compute_answer():
        articles = [{'type': 'article',
                        'id': 'abc', 'title': query_string, 'message_text': query_string}]

        return articles

    answerer.answer(msg, compute_answer)

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)


TOKEN = setting.token  # get token from setting file

bot = telepot.async.Bot(TOKEN)
answerer = telepot.async.helper.Answerer(bot)

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop({'chat': on_chat_message,
                                   'callback_query': on_callback_query,
                                   'inline_query': on_inline_query,
                                   'chosen_inline_result': on_chosen_inline_result}))
print('Listening ...')

loop.run_forever()
