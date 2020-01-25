#!/usr/bin/python3
from telegram.ext import Updater,MessageHandler,Filters,Dispatcher
import telegram
import time
from os import system
import os
import car
import threading
import configparser

bot_id = 1#input("請輸入程序執行ID : ")
bot_id = int(bot_id)
# 從config.ini文件加載數據
config = configparser.ConfigParser()
config.read('config.ini')

# 機器人ACCESS_TOKEN
TOKEN = config['TELEGRAM']['ACCESS_TOKEN']




# mysql data

# 主機位置
server_host = config['mysql']['server_host']
# 使用者名稱
username = config['mysql']['username']
# 密碼
password = config['mysql']['password']
# 資料庫名稱
from_port = config['mysql']['from_port']
user_id = 726651325
time.sleep(5)
bot = telegram.Bot(token=TOKEN)
Open = True
DELAY_TIME = 0.5
#資料更新副程序啟動
def data_update():
    global Open
    while Open:
        if(not car.updata()):
            bot.send_message(user_id,'私服器連接失敗...重連中')
            car.Start(  
                bot_id = bot_id,
                host = server_host,
                user = username,
                password = password,
                database = from_port
        )
            bot.send_message(user_id,'私服器連接成功')
        time.sleep(DELAY_TIME)

#連結資料庫
variable = car.Start(  
  bot_id = bot_id,
  host = server_host,
  user = username,
  password = password,
  database = from_port
)
if(variable == False):
    bot.send_message(user_id,'發生錯誤 -- 機器人預設數值為空\n請 @abab5601 手動重啟')
    car.log(bot_id,0,99,"發生錯誤 -- 機器人預設數值為空")
    car.stop()
    os._exit(1)
#潛水判定訊息數
death_message = int(variable[4][0])
#潛水判定天數
death_day = int(variable[5][0])
#備份群id
Backup = int(variable[6][0])
# 建立一個子執行緒
t = threading.Thread(target = data_update)
t.start()
#t.start()
bot.send_message(user_id,'機器編號 - %s : 啟動完成'%(bot_id))
while True:
    point = car.point_vip_members_delete()
    if(not point[0] and point[1] == -2):
        None
    elif (point[0]):
        for user in point[1]:
            bot.kick_chat_member(Backup,user[0])
            car.vip_group_members(user[0],0)
            bot.send_message(user[0],'你因為連續 %s 天積分未達成 %s 因此取消你vip群資格\n如要重新進入與原入群方式相同'%(death_message,death_day))
            car.log(user[0],user[0],2,'以溺水,踢出群組')
        for user in point[2]:
            bot.send_message(user[0],'你已經快溺水了,請達到每日積分標準,要不會強制踢出vip群\n你剩餘%s天'%(user[1]))
            car.log(user[0],user[0],3,'溺水提醒倒數%s天'%(user[1]))
        car.log(bot_id,0,98,'今日vip群剔除人數 : %s 人, 今日警告人數 : %s 人 今日日期 : %s 清單 : %s , %s'%(len(point[1]),len(point[2]),str(point[3]),point[1],point[2]))
    elif (not point[0] and point[1] == -404):
        car.Start(  
        bot_id = bot_id,
        host = server_host,
        user = username,
        password = password,
        database = from_port,
        )
    else:
        car.log(bot_id,bot_id,99,'發生錯誤 : 無法取得變數')
        bot.send_message(user_id,'發生錯誤 -- 機器人預設數值為空\n請 @abab5601 手動重啟')
        car.stop()
        os._exit(1)
    
    message = car.delete_message()
    if(not message[0]):
        car.Start(  
                bot_id = bot_id,
                host = server_host,
                user = username,
                password = password,
                database = from_port,
            )
    elif(message[1]):
        for i in message[1]:
            try:
                bot.deleteMessage(i[0],i[1])
                car.log(i[0],bot_id,i[1],'訊息已刪除')
            except:
                car.log(i[0],bot_id,i[1],'訊息無法刪除1')
                time.sleep(DELAY_TIME*2)
                try:
                    bot.deleteMessage(i[0],i[1])
                    car.log(i[0],bot_id,i[1],'訊息已刪除')
                except:
                    car.log(i[0],bot_id,i[1],'訊息無法刪除2')
    time.sleep(DELAY_TIME)