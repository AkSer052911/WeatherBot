#connect all the necessary libraries
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
import re
import time 



#get our token
from config import TOKEN


############################
#our parser code
from selenium import webdriver

website = "https://www.accuweather.com" #the site from which we will find out the weather(You can choose another one, but then the code will be different)
browser = webdriver.Chrome()
browser.get(website)
search_bar = browser.find_element_by_class_name("search-input")
search_button = browser.find_element_by_class_name("search-icon")
perfomed_to_the_first_time = True
page_now = "now"


       




############################






#configure logging
logging.basicConfig(level=logging.INFO)

#create a bot object
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_weather_at_this_moment():
       global page_now
       if page_now != "now":
              browser.get(browser.find_elements_by_class_name("subnav-item")[0].get_attribute("href"))
              page_now = "now"

       buttons = browser.find_elements_by_class_name("subnav-item")
       text = browser.find_element_by_class_name("lbar-panel").text
       return text
def get_weather_hourly():
       global page_now
       if page_now != "hourly":
              browser.get(browser.find_elements_by_class_name("subnav-item")[1].get_attribute("href"))
              page_now = "hourly"
       elements = browser.find_elements_by_class_name("non-ad")
       return elements


def get_weather_daily():
       global page_now
       if page_now != "daily":
              browser.get(browser.find_elements_by_class_name("subnav-item")[2].get_attribute("href"))
              page_now = "daily"
       elements = browser.find_elements_by_class_name("daily-forecast-card ")
       return elements

       
def get_url_by_location(location):
       global page_now
       global buttons
       global perfomed_to_the_first_time
       if perfomed_to_the_first_time == True:
              search_bar.send_keys(str(location))
              search_button.click()
       else:
              search_bar2 =  browser.find_element_by_class_name("search-input")
              search_button2 = browser.find_element_by_class_name("icon-search")
              search_bar2.send_keys(str(location))
              search_button2.click()
       perfomed_to_the_first_time = False
       page_now = "now"
       


#creating a greeting for our bot
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
       await message.reply("Hi! I'm a weather bot!\nYou can use me to view the weather forecast without leaving Telegram.\nFirst, specify your region in the 'region-country'.\n You can always change your region simply by writing a message with your region")

	
@dp.message_handler(commands=['weathernow'])
async def send_now_weather_comand(msg: types.Message):
       await bot.send_message(msg.from_user.id,get_weather_at_this_moment())
       
@dp.message_handler(commands=['weatherhourly'])
async def send_now_weather_comand(msg: types.Message):
       for elem in get_weather_hourly():
              await bot.send_message(msg.from_user.id,elem.text)

@dp.message_handler(commands=['weatherdaily'])
async def send_now_weather_comand(msg: types.Message):
       for elem in get_weather_daily():
              await bot.send_message(msg.from_user.id,elem.text)
       

@dp.message_handler()
async def echo(message: types.Message):
       try:
              get_url_by_location(message.text)
       except:
              print("Some problems")

#create an infinite loop for constant bot operation
if __name__ == '__main__':
    executor.start_polling(dp)

