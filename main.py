import telepot
import setting

bot = telepot.Bot(setting.token)
response = bot.getUpdates()
print(response)
