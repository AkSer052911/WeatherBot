#connect all the necessary libraries
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
import re




#get our token
from config import TOKEN


############################
#our parser code

import requests
from bs4 import BeautifulSoup as bs

headers= {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.282"}
r = requests.get('https://www.gismeteo.com', headers=headers)
soup = bs(r.text,"lxml")
s1 = soup.find("div",class_="weather_now")
now_weather = s1.text
nw = s1.text.split("\n")
nw.pop(13)
nw.pop(34)

for i in range(len(nw)):
       print(nw[i])

       
for i in range(len(nw)):
       nw[i] = re.sub(r'\s', '', nw[i])
now_weather = ' '.join(nw)






############################










#configure logging
logging.basicConfig(level=logging.INFO)

#create a bot object
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


#creating a greeting for our bot
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
	await message.reply("Hi! I'm a weather bot!\nYou can use me to view the weather forecast without leaving Telegram ")

	
#Our main command to check weather
@dp.message_handler(commands=['weathernow'])
async def send_nowweather_comand(msg: types.Message):
        await bot.send_message(msg.from_user.id,now_weather)




#create an infinite loop for constant bot operation
if __name__ == '__main__':
    executor.start_polling(dp)

