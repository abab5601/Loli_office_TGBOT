#!/usr/bin/python3
from telegram.ext import Updater,MessageHandler,Filters,Dispatcher
import telegram
import time
from os import system
import os
import car
import threading
bot_id = 1#input("請輸入程序執行ID : ")
bot_id = int(bot_id)
TOKEN='999287984:AAH_NBTaLC8hvSLkr_S07vgWRAnwu_AiwTI'#'907913554:AAG52RAzo6Fctp-1NDTQAbeudQnMwMKwlMs'
# TOKEN = '907913554:AAG52RAzo6Fctp-1NDTQAbeudQnMwMKwlMs'  # test
#mysql data
# 主機位置
server_host = '192.168.1.123'
#使用者名稱
username = 'LoliOfficeBot'
#密碼
password = 'abab5610'
#資料庫名稱
from_port = 'LoliOfficeBot'
user_id = 726651325
# time.sleep(5)
# bot = telegram.Bot(token=TOKEN)
# Open = True
# DELAY_TIME = 0.5
# #資料更新副程序啟動
# def data_update():
#     global Open
#     while Open:
#         if(not car.updata()):
#             bot.send_message(user_id,'私服器連接失敗...重連中')
#             car.Start(  
#                 bot_id = bot_id,
#                 host = server_host,
#                 user = username,
#                 password = password,
#                 database = from_port
#         )
#             bot.send_message(user_id,'私服器連接成功')
#         time.sleep(DELAY_TIME)

#連結資料庫
variable = car.Start(  
  bot_id = bot_id,
  host = server_host,
  user = username,
  password = password,
  database = from_port
)
# if(variable == False):
#     bot.send_message(user_id,'發生錯誤 -- 機器人預設數值為空\n請 @abab5601 手動重啟')
#     car.log(bot_id,0,99,"發生錯誤 -- 機器人預設數值為空")
#     car.stop()
#     os._exit(1)


# print(car.get_car(123 , "5"))
# i="aawa"
# print(i.find('wa'))

car.blacklist_status(860187237,True,1000)