#!/usr/bin/python3
import sys
from telegram.ext import Updater, MessageHandler, Filters, Dispatcher
import telegram
import time
from os import system
import os
import car
import threading
import configparser

################################################################
bot_id = 0  # input("請輸入程序執行ID : ")
bot_id = int(bot_id)
# 管理者姓名
username = '備份群'
# 管理者ID
user_id = 726651325
#引入資料
# 從config.ini文件加載數據
config = configparser.ConfigParser()
config.read('config.ini')

DELAY_TIME = 0.5
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
################################################################
# 機器人宣告
time.sleep(5)
# time.sleep(5)
# 開車人資料站存區
car_user = [None]
# 限時對話資料暫存區
time_message = [None]
# 程式執行中
Open = True

# 連結資料庫
variable = car.Start(
    bot_id=bot_id,
    host=server_host,
    user=username,
    password=password,
    database=from_port
)
bot = telegram.Bot(token=TOKEN)
if(variable == False):
    bot.send_message(user_id, '發生錯誤 -- 機器人預設數值為空\n請 @abab5601 手動重啟')
    car.log(bot_id, 0, 99, "發生錯誤 -- 機器人預設數值為空")
    car.stop()
    os._exit(1)
# 開車時間
Failure_time = int(variable[0][0])
# 聊天室車刪除時間
car_time = int(variable[1][0])
# 訂閱列表
subscription = eval(variable[3][0])
# 潛水判定訊息數
death_message = int(variable[4][0])
# 潛水判定天數
death_day = int(variable[5][0])
# 備份群id
Backup = int(variable[6][0])
# 活動用關鍵字
Keywords = variable[8][0]
################################################################
# 資料更新副程序啟動


def data_update():
    global Open
    global variable
    while Open:
        if(not car.updata()):
            bot.send_message(user_id, '私服器連接失敗...重連中')
            variable = car.Start(
                bot_id=bot_id,
                host=server_host,
                user=username,
                password=password,
                database=from_port
            )
            bot.send_message(user_id, '私服器連接成功')
            # 開車時間
            Failure_time = int(variable[0][0])
            # 聊天室車刪除時間
            car_time = int(variable[1][0])
            if(Failure_time == None or car_time == None):
                bot.send_message(
                    user_id, '發生錯誤 -- 機器人預設數值為空\n請 @abab5601 手動重啟')
                sys.exit(1)
        time.sleep(DELAY_TIME)


def reboot():
    for i in range(5, -1, -1):
        print('重開機倒數計時 - %s' % (i))
        if i == 0:
            global system
            system('reboot')
        time.sleep(1)


# 建立一個子執行緒
t = threading.Thread(target=data_update)
t.start()
bot.send_message(user_id, '機器編號 - %s : 啟動完成' % (bot_id))
# 主程式
# 查詢開車狀態

updater = Updater(token=TOKEN)

# 版面清洗
if os.name == 'nt':
    system('cls')  # win 用
    print('use win system')
elif os.name == 'posix':
    system('clear')  # linux 用
    print('use linux system')


def caruser(title, user):
    global car_user
    try:
        if title == car_user[0] and user == car_user[1] and car_user[2] >= time.time():
            return True
    except:
        None
    NewTime = car.get_car_user(title, user)
    if(NewTime == -1):
        car.Start(
            bot_id=bot_id,
            host=server_host,
            user=username,
            password=password,
            database=from_port,
        )
        NewTime = car.get_car_user(title, user)
        if(NewTime == -1):
            return False
    car_user = [title, user, NewTime]
    if title == car_user[0] and user == car_user[1] and car_user[2] >= time.time():
        return True
    return False
# 現實訊息(未啟用)


def timemessage(chat):
    global time_message
    try:
        if time_message[0] == chat and time_message[1] >= time.time():
            return True
    except:
        NewTime = car.get_car_user(chat, chat)
        time_message = [chat, NewTime]
        if time_message[0] == chat and time_message[1] >= time.time():
            return True
    return False
# 取得服務群組名單


def get_subscriber(chat_id, find=False):
    global subscription
    ls = subscription[:]
    try:
        ls.remove(chat_id)
    except:
        if(find):
            return False
    return ls


#################################
def getVideo(bot, update):
    if update.message.chat.id == -340691240:
        car.new_car_data(update.message.video.file_id, 0)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, '車庫補貨', update.message.video.file_id)
        update.message.reply_text("OK")
        return True
    if update.message.caption:
        caption = update.message.caption
    else:
        caption = ""
    bot.send_video(user_id, update.message.video, caption="%s,%s,%s,%s"
                   % (str(update.message.chat.id), str(update.message.message_id), str(time.time()), str(update.message.caption)))
    if caruser(update.message.chat.id, update.message.from_user.id) or ('/car' in caption):
        car.new_car(update.message.chat.id, update.message.message_id)
        car.point(update.message.from_user.id)
        car.point(update.message.from_user.id)
        if '/car' in caption:
            message = bot.send_message(
                update.message.chat.id, '倒數%s秒後刪除' % (car_time))
            car.check_message(message.chat.id, message.message_id, 7)
        if update.message.chat.id == -1001278835291:
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "傳送了影片(開車)", str(update.message.video.file_id))
        else:
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "傳送了影片(匿名開車)", str(update.message.video.file_id))
        for user in get_subscriber(update.message.chat.id):
            message = bot.send_video(
                user, update.message.video, caption=update.message.caption)
            if(user == -1001278835291):
                car.new_car(message.chat.id, message.message_id)
            car.log(message.chat.id, update.message.from_user.id,
                    message.message_id, '接收影片')
    else:
        if get_subscriber(update.message.chat.id, True):
            car.point(update.message.from_user.id)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, "傳送了影片", update.message.video.file_id)


photos = []


def getPhoto(bot, update):
    if update.message.caption:
        caption = update.message.caption
    else:
        caption = ""
    photo_ = update.message.photo[0]
    for photo in update.message.photo:
        if photo.file_size > photo_.file_size:
            photo_ = photo

    if update.message.chat.id == -340691240:
        photos.append(photo_.file_id)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, '車庫補貨', photo_.file_id)
        update.message.reply_text("OK")
        return True

    bot.send_photo(user_id, photo_, caption="%s,%s,%s,%s"
                   % (str(update.message.chat.id), str(update.message.message_id), str(time.time()), str(update.message.caption)))
    if caruser(update.message.chat.id, update.message.from_user.id) or '/car' in caption:
        car.new_car(update.message.chat.id, update.message.message_id)
        car.point(update.message.from_user.id)
        car.point(update.message.from_user.id)
        if '/car' in caption:
            message = bot.send_message(
                update.message.chat.id, '倒數%s秒後刪除' % (car_time))
            car.check_message(message.chat.id, message.message_id, 7)
        if update.message.chat.id == -1001278835291:
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "傳送了照片(開車)", photo_.file_id)
        else:
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "傳送了照片(匿名開車)", photo_.file_id)
        for user in get_subscriber(update.message.chat.id):
            message = bot.send_photo(
                user, photo_, caption=update.message.caption)
            if(user == -1001278835291):
                car.new_car(message.chat.id, message.message_id)
            car.log(message.chat.id, update.message.from_user.id,
                    message.message_id, '接收照片')
    else:
        if get_subscriber(update.message.chat.id, True):
            car.point(update.message.from_user.id)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, "傳送了照片", photo_.file_id)


def getDocument(bot, update):
    if update.message.chat.id == -340691240:
        car.new_car_data(update.message.document.file_id, 2)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, '車庫補貨', update.message.document.file_id)
        update.message.reply_text("OK")
        return True
    if update.message.caption:
        caption = update.message.caption
    else:

        caption = ""
    bot.send_document(user_id, update.message.document, caption="%s,%s,%s,%s"
                      % (str(update.message.chat.id), str(update.message.message_id), str(time.time()), str(update.message.caption)))
    if caruser(update.message.chat.id, update.message.from_user.id) or '/car' in caption:
        car.new_car(update.message.chat.id, update.message.message_id)
        car.point(update.message.from_user.id)
        car.point(update.message.from_user.id)
        if '/car' in caption:
            message = bot.send_message(
                update.message.chat.id, '倒數%s秒後刪除' % (car_time))
            car.check_message(message.chat.id, message.message_id, 7)
        if update.message.chat.id == -1001278835291:
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "傳送了檔案(開車)", update.message.document.file_id)
        else:
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "傳送了檔案(匿名開車)", update.message.document.file_id)
        for user in get_subscriber(update.message.chat.id):
            message = bot.send_document(
                user, update.message.document, caption=update.message.caption)
            if(user == -1001278835291):
                car.new_car(message.chat.id, message.message_id)
            car.log(message.chat.id, update.message.from_user.id,
                    message.message_id, '接收檔案', message.document.file_id)
    else:
        if(get_subscriber(update.message.chat.id, True)):
            car.point(update.message.from_user.id)
        car.log(update.message.chat.id, message.from_user.id,
                update.message.message_id, "傳送了檔案", update.message.file_id)


def getmessage(bot, update):
    if get_subscriber(update.message.chat.id, True) and Keywords != "":
        if update.message.text.find(Keywords) != -1:
            x = None
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "參加活動")
            value = car.get_car(update.message.from_user.id, Keywords)
            if value == -1:
                bot.send_message(726651325, "活動觸發錯誤")
            if value == -2:
                x = update.message.reply_text("已領取過此次活動")
                car.log(update.message.chat.id,
                        update.message.from_user.id, x.id, "已領取過此次活動")
            elif value == -3:
                x = update.message.reply_text("這次車已領完~\t下次請早")
                car.log(update.message.chat.id,
                        update.message.from_user.id, x.id, "活動獎勵已領完")
                x = bot.send_message(-340691240, "活動用車已用完")
                car.log(x.char.id, x.from_user.id, x.message_id, "通知活動用車已用完")
            else:
                car.point(update.message.from_user.id)
                car.point(update.message.from_user.id)
                car.point(update.message.from_user.id)
                car.point(update.message.from_user.id)
                car.point(update.message.from_user.id)
                x = update.message.reply_text("恭喜獲得車\t感謝參加活動")
                car.log(update.message.chat.id, update.message.from_user.id,
                        x.message_id, "成功領取活動獎勵 活動關鍵字%s" % (Keywords))
                if value[2] == 0:  # 影片
                    bot.send_video(user_id, value[1], caption="%s,%s,%s,%s"
                                   % (str(update.message.chat.id), str(update.message.message_id), str(time.time()), "%s活動獎勵" % (update.message.from_user.name)))

                    for user in get_subscriber(0):
                        message = bot.send_video(
                            user, value[1], caption="%s 活動獎勵" % (update.message.from_user.name))
                        if(user == -1001278835291):
                            car.new_car(message.chat.id, message.message_id)
                        car.log(message.chat.id, update.message.from_user.id,
                                message.message_id, '活動發車(影片)', value[1])
                elif value[2] == 1:
                    for car_find in eval(value[1]):
                        print(car_find)
                        bot.send_photo(user_id, car_find, caption="%s,%s,%s,%s"
                                       % (str(update.message.chat.id), str(update.message.message_id), str(time.time()), "%s活動獎勵" % (update.message.from_user.name)))
                        for user in get_subscriber(0):
                            message = bot.send_photo(
                                user, car_find, caption="%s活動獎勵" % (update.message.from_user.name))
                            if(user == -1001278835291):
                                car.new_car(message.chat.id,
                                            message.message_id)
                            car.log(message.chat.id, update.message.from_user.id,
                                    message.message_id, '活動發車(照片)', value[1])
                elif value[2] == 2:
                    bot.send_document(user_id, value[1], caption="%s,%s,%s,%s"
                                      % (str(update.message.chat.id), str(update.message.message_id), str(time.time()), "%s活動獎勵" % (update.message.from_user.name)))
                    for user in get_subscriber(0):
                        message = bot.send_document(
                            user, value[1], caption="%s活動獎勵" % (update.message.from_user.name))
                        if(user == -1001278835291):
                            car.new_car(message.chat.id, message.message_id)
                        car.log(message.chat.id, update.message.from_user.id,
                                message.message_id, '活動發車(檔案)', value[1])
            car.check_message(update.message.char.id, x.message_id, 10)
    if caruser(update.message.chat.id, update.message.from_user.id) or '/car' in update.message.text:
        car.point(update.message.from_user.id)
        car.point(update.message.from_user.id)
        if caruser(update.message.chat.id, update.message.from_user.id):
            car.new_car(update.message.chat.id, update.message.message_id)
        if '/car' in update.message.text:
            message = bot.send_message(
                update.message.chat.id, '倒數%s秒後刪除' % (car_time))
            car.check_message(message.chat.id, message.message_id, 7)
        if update.message.chat.id == -1001278835291:
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "傳送了訊息(開車)", update.message.text)

        else:
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "傳送了匿名訊息(開車)", update.message.text)

        # 轉車
        for user in get_subscriber(update.message.chat.id):
            message = bot.send_message(user, update.message.text)
            if(user == -1001278835291):
                car.new_car(message.chat.id, message.message_id)
            car.log(user, update.message.from_user.id,
                    message.message_id, '接收訊息')
    else:
        if (get_subscriber(update.message.chat.id, True)):
            car.point(update.message.from_user.id)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, "傳送了%s" % (update.message.text))
######################


def SetInstruction_processing(bot, update):
    global car_user
    global Failure_time
    global photos
    global car_user
    text = str(update.message.text)
    car.update_user(update.message.from_user.id, update.message.from_user.username,
                    update.message.from_user.last_name, update.message.from_user.first_name)
    if '/save_photos' == text[0:12]:
        if photos != []:
            car.new_car_data(photos, 1)
            photos = []
            update.message.reply_text("OK")
        else:
            update.message.reply_text("沒資料")
    elif '/start_car' == text[0:10]:
        dd = car.blacklist(update.message.from_user.id)
        if dd == -1:
            car.Start(bot_id, server_host, username, password, from_port)
            dd = car.blacklist(update.message.from_user.id)
        if(dd):
            x = bot.send_message(
                update.message.chat.id, "你現在無法發車,你濫用機器人遭封鎖.\n%s解除封鎖\n如有疑問請尋找管理員 @abab5601" % (dd))
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "黑名單要求開車")
            car.check_message(x.chat.id, x.message_id, 7)
            bot.deleteMessage(update.message.chat.id,
                              update.message.message_id)
            return True
        if not car.start_car(update.message.chat.id, update.message.from_user.id):
            bot.send_message(user_id, '發車錯誤\n頻道 : %s 使用者 : %s' % (
                update.message.chat.id, update.message.from_user.id))
            d = update.message.reply_text('無法發車--請重試\n多次無發發車請通知管理員 @abab5601')
            car.check_message(update.message.chat.id,
                              update.message.message_id, 7)
            car.check_message(d.chat.id, d.message_id, 7)
            return False
        id_ = update.message.from_user.name
        car_user = [update.message.chat.id,
                    update.message.from_user.id, time.time()+Failure_time]
        message = bot.send_message(update.message.chat.id, '%s 你可以了開車\n我可以幫你收車\n開車時間至%s'
                                   % (id_, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+Failure_time))))
        car.check_message(message.chat.id, message.message_id, 7)
        message = bot.send_message(
            update.message.chat.id, '#發車記錄點!(開始)%s' % (update.message.from_user.name))
        car.new_car(update.message.chat.id, message.message_id)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, '開始開車')
    elif '/car' == text[0:4]:
        car.new_car(update.message.chat.id, update.message.message_id)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, '發送資源\n%s' % (update.message.text))
        message = bot.send_message(
            update.message.chat.id, '倒數%s秒後刪除' % (car_time))
        car.check_message(message.chat.id, message.message_id, 7)
    elif '/stop_car' == text[0:9]:
        ren = car.stop_car(update.message.chat.id, update.message.from_user.id)
        if ren == -1:
            car.Start(
                bot_id=bot_id,
                host=server_host,
                user=username,
                password=password,
                database=from_port
            )
            ren = car.stop_car(update.message.chat.id,
                               update.message.from_user.id)
            if(ren == -1):
                bot.send_message(user_id, '發生錯誤:\n頻道 : %s 使用者 : %s' % (
                    update.message.chat.id, update.message.from_user.id))
                update.message.reply_text('無法停止發車--請重試\n多次無發發車請通知管理員')
                return False
        if ren and ren != -1:
            car_user = [update.message.chat.id,
                        update.message.from_user.id, time.time()]
            message = bot.send_message(
                update.message.chat.id, '停止\n資源時間到會自動刪除')
            car.check_message(message.chat.id, message.message_id, 10)
            message = bot.send_message(
                update.message.chat.id, '#發車記錄點!(結束)%s' % (update.message.from_user.name))
            car.new_car(update.message.chat.id, message.message_id)
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, '停止發車')
        elif ren != -1:
            message = bot.send_message(update.message.chat.id, '你沒有正在開車')
            car.check_message(message.chat.id, message.message_id, 5)
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, '停止發車無效')
    elif '/status_car' == text[0:11]:
        id_ = update.message.from_user.name
        if caruser(update.message.chat.id, update.message.from_user.id):
            message = bot.send_message(
                update.message.chat.id, '%s 現在開車狀態 : 開車中' % (id_))
            car.check_message(message.chat.id, message.message_id, 5)
        else:
            message = bot.send_message(
                update.message.chat.id, '%s 現在開車狀態 : 休息中' % (id_))
            car.check_message(message.chat.id, message.message_id, 5)
    elif '/黑名單' == text[0:4]:
        admin = False
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, "要求封鎖黑名單")
        if(update.message.reply_to_message):
            blacklist_id = car.messageLookFor(
                update.message.chat.id, update.message.reply_to_message.message_id)
            if(blacklist_id == -2):
                a = bot.send_message(update.message.chat.id,
                                     "操作太快請稍後重試\n如多次錯誤請通知管理員")
                car.log(update.message.chat.id, a.from_user.id,
                        a.message_id, "封鎖錯誤 : 找不到訊息ID")
                car.check_message(a.chat.id, a.message_id, 7)
                car.check_message(update.message.chat.id,
                                  update.message.message_id, 7)
                return False
        else:
            a = bot.send_message(update.message.chat.id, "指令使用錯誤\n請回復要黑名單的訊息")
            car.log(update.message.chat.id, a.from_user.id,
                    a.message_id, "封鎖錯誤 : 指令格式錯誤")
            car.check_message(a.chat.id, a.message_id, 7)
            car.check_message(update.message.chat.id,
                              update.message.message_id, 7)
            return False
        if(blacklist_id == bot.id):
            bot.send_message(update.message.chat.id, "此訊息由機器人主動發出(非匿名發車),無法封鎖")
            a = bot.deleteMessage(update.message.chat.id,
                                  update.message.message_id)
            car.log(update.message.chat.id, a.from_user.id,
                    a.message_id, "封鎖錯誤 : 機器人訊息")
            car.check_message(a.chat.id, a.message_id, 7)
            car.check_message(update.message.chat.id,
                              update.message.message_id, 7)
            return False
        for x in bot.get_chat_administrators(-1001278835291):
            if(x.user.id == blacklist_id):
                a = bot.send_message(update.message.chat.id,
                                     "錯誤 : 無發封鎖管理員\n請聯絡 @abab5601")
                car.log(update.message.chat.id, a.from_user.id,
                        a.message_id, "封鎖錯誤 : 無法封鎖管理員 %s" % (blacklist_id))
                bot.deleteMessage(update.message.chat.id,
                                  update.message.message_id)
                car.check_message(a.chat.id, a.message_id, 7)
                return False
            elif(x.user.id == update.message.from_user.id):
                admin = True
        The_reason, DD, Day = text[4:].replace(" ", "").partition(':')
        try:
            f = int(Day)
        except ValueError:
            f = 0
        if(DD != ':' and (f < -1)):
            a = bot.send_message(update.message.chat.id,
                                 "指令發送錯誤\n格式 : \n/黑名單 封鎖原因 : 天數 \n如日期為永久則輸入-1\n取消黑名單天數輸入0")
            car.log(update.message.chat.id, a.from_user.id,
                    a.message_id, "封鎖錯誤 : 指令格式錯誤")
            bot.deleteMessage(update.message.chat.id,
                              update.message.message_id)
            car.check_message(update.message.chat.id,
                              update.message.message_id, 7)
            car.check_message(a.chat.id, a.message_id, 7)
            return False
        da = bot.get_chat_member(update.message.chat.id, blacklist_id)
        if(not admin):
            c = bot.send_message(update.message.chat.id,
                                 "你不是管理員無法封鎖\n以幫你向管理員檢舉")
            car.log(update.message.chat.id, c.from_user.id,
                    c.message_id, "封鎖錯誤 : 不是管理員 想封鎖對象 , 回復")
            d = bot.send_message(-1001215609662, "%s檢舉%s請確認\n群組名稱 : %s\n原因 : %s" %
                                 (update.message.from_user.name, da.user.name, update.message.chat.title, The_reason))
            car.log(-1001215609662, d.from_user.id,
                    d.message_id, "封鎖錯誤 : 不是管理員 想封鎖對象 : %s" % (blacklist_id))
            bot.deleteMessage(update.message.chat.id,
                              update.message.message_id)
            car.check_message(c.chat.id, c.message_id, 7)
            return False
        if(not car.blacklist_status(blacklist_id, True, f)):
            a = bot.send_message(update.message.chat.id,
                                 "錯誤 : \n系統錯誤")
            car.log(update.message.chat.id, a.from_user.id,
                    a.message_id, "封鎖失敗 %s" % (blacklist_id))
            car.check_message(a.chat.id, a.message_id, 7)
        else:
            car_user[3] = time.time()-1
            car.point_Reset(blacklist_id)
            car.stop_car(1, update.message.from_user.id)
            a = update.message.reply_text("已成功封鎖")
            car.log(update.message.chat.id, a.from_user.id,
                    a.message_id, "新增黑名單成員 : %s 因%s被%s封鎖%s天" % (blacklist_id, The_reason, update.message.from_user.name, Day))
            car.check_message(a.chat.id, a.message_id, 7)
            car.check_message(update.message.chat.id,
                              update.message.message_id, 7)
            for user in get_subscriber(0):
                message = bot.send_message(
                    user, "%s因為%s被封鎖%s天" % (da.user.name, The_reason, Day))
                car.log(user, update.message.from_user.id,
                        message.message_id, '發送%s因為%s被封鎖%s天訊息' % (da.user.name, The_reason, Day))
            bot.send_message(-1001215609662, "%s因為%s被封鎖%s天" %
                             (da.user.name, The_reason, Day))
        return True

    elif '/GetID' == text[0:6]:
        bot.send_message(update.message.chat.id, '頻道     ID : '+str(
            update.message.chat.id)+'\n使用者 ID : '+str(update.message.from_user.id))
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, '取得ID')
        bot.deleteMessage(update.message.chat.id, update.message.message_id)
    elif '/time_message' == text[0:13]:
        bot.deleteMessage(update.message.chat.id, update.message.message_id)
        car.start_car(update.message.chat, update.message.chat)
        message = bot.send_message(update.message.chat, '群組開始進入限時對話\n限時對話將於%s結束或是手動關閉\n限時對話 : 每則訊息會在發出後的%s秒後刪除'
                                   % (str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+Failure_time))), str(car_time)))
        car.check_message(message.chat.id, message.message_id, car_time)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, '開啟限時對話')
    elif '/stop_time_message' == text[0:18]:
        bot.deleteMessage(update.message.chat.id, update.message.message_id)
        if car.stop_car(update.message.chat.id, update.message.from_user.id):
            message = bot.send_message(
                update.message.chat, '已恢復正常對話模式\n限時對話模式中的訊息會在倒數計時到後刪除')
            car.check_message(message.chat.id, message.message_id, 5)
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, '結束限時對話')
        else:
            message = bot.send_message(update.message.chat, '頻道未開啟限時對話')
            car.check_message(message.chat.id, message.message_id, 5)
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, '結束限時對話失敗')
    elif '/status_time_message' == text[0:20]:
        if timemessage(update.message.chat.id):
            message = bot.send_message(update.message.chat.id, '對話狀態 : 限時對話')
            car.check_message(message.chat.id, message.message_id, 5)
        else:
            message = bot.send_message(update.message.chat.id, '對話狀態 : 正常狀態')
            car.check_message(message.chat.id, message.message_id, 5)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, "查詢頻道狀態")
    elif '/status_point' == text[0:13]:
        re = bot.get_chat_member(Backup, update.message.from_user.id)
        if(re.status == 'member' or re.status == 'restricted' or re.status == 'administrator'):
            car.vip_group_members(update.message.from_user.id, 1)
        else:
            car.vip_group_members(update.message.from_user.id, 0)
        ls = car.point_vip_get(update.message.from_user.id)
        if(update.message.chat.id < 0):
            message = bot.send_message(update.message.chat.id, "請在私人聊天室查詢")
            car.check_message(message.chat.id, message.message_id, 2)
        elif(ls[1] == 1):
            if ls[0] > 0:
                bot.send_message(update.message.chat.id, "你已在群組內\n 今日差 %s 分浮出水面 \n 每日所需最低積分 : %s" % (
                    ls[0], death_message))
                car.log(update.message.chat.id, update.message.from_user.id,
                        update.message.message_id, '使用者查詢vip資格 : 已在群內 -- 今日積分未達成 差 %s 分' % (ls[0]))
            else:
                ls[0] -= death_message
                ls[0] *= -1
                bot.send_message(update.message.chat.id, "你已在群組內\n 今日積分已達 %s 分 \n 每日所需最低積分 : %s\n已達成今日所需!" % (
                    ls[0], death_message))
                car.log(update.message.chat.id, update.message.from_user.id,
                        update.message.message_id, '使用者查詢vip資格 : 已在群內 -- 今日積分已達成 %s 分' % (ls[0]))
        elif ls[0] <= 0:
            id_ = update.message.from_user.id
            bot.send_message(update.message.chat.id, "你好歡迎進入群組\n群組規則 : 只要積分未達%s分連續%s天將會被強制剔除\n請在今日24點前進入\n連結 : %s" % (
                death_message, death_day, str(bot.export_chat_invite_link(Backup))))
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "申請進入群組(完成)")
            try:
                bot.unban_chat_member(Backup, id_)
            except:
                pass
        else:
            bot.send_message(update.message.chat.id, "你在%s分即可進入備份群" % (ls[0]))
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, "無法進入vip群 缺少積分 : %s" % (ls[0]))
    elif '/start' == text[0:6]:
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, '查詢機器人指令')
        message = bot.send_message(update.message.chat.id, '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % (
            '機器人指令列表 :',
            '/start               : 查看所有指令',
            '/start_car       : 開始發大量資源 \n-->發完指令後你個人發的訊息在特定時間內都會算做資源',
            #'/car                  : 發網址資源(指令只能發在訊息的第一行,同一則訊息才算)',
            '/status_car     : 查詢目前開車狀態',
            '/stop_car        : 與 /start_car 關聯\n-->發完資源後回復正常對話模式\n',
            #'/time_message              : 在此模式下期間,所有訊息會被刪除',
            #'/status_time_message : 查詢目前對話模式',
            #'/stop_time_message    : 與 /time_message 搭配\n-->用於提早結束限時對話模式\n',
            '新備份群機制說明 :\n因備份群公開後經常被舉報群組掛掉\n因此現在改積分制管理',
            '\n累計積分方法:\n在群內發車(2分)或聊天一則訊息(1分)-指令除外\n使用機器人匿名發車一台車2分(匿名開車教學往下看)\n積分會在每日24奌扣%s\n\n進群發法:\n使用查詢活躍度指令當積分足夠會得到群網址' % (death_message),
            '\n備份群規範 : \n進群須達積分%s分才可進入\n進入後如%s天以上未達%s分會被強制剔除!\n(如被剔除重進方法: 與進群方法相同)(積分上限 : 1000)' % (
                death_message, death_day, death_message),
            '/status_point       :查詢活躍度',
            '與機器人的對話將在 60 秒後刪除\n機器人開發者 : @abab5601',
            '目前機器人剛開發完成有BUG或其他問題情直接聯繫開發者',
            # 點名 : 自動通知群內溺水的人起來呼吸(說警告比較貼切)'
            '新增功能 : \n匿名發車 :　 再羅咖以外的聊天室發 /start_car 即可開始發車\n'
        ))
        car.check_message(message.chat.id, message.message_id, 60)

    elif '/reboot' == text[0:7]:
        if((update.message.chat.id == user_id) or (update.message.chat.id == -1001297029945)):
            bot.send_message(update.message.chat.id, 'ok')
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, '重新啟動 - %s' % (bot_id))
            if os.name == 'posix':
                t = threading.Thread(target=reboot)
                t.start()
                car.stop()
            else:
                bot.send_message(update.message.chat.id,
                                 '重啟失敗:目前使用系統 = win system')
        else:
            bot.send_message(update.message.chat.id, '權限不足')
            car.log(update.message.chat.id, update.message.from_user.id,
                    update.message.message_id, '呼叫重新啟動')
    else:
        car.check_message(update.message.chat.id, update.message.message_id, 5)
        message = bot.send_message(
            update.message.chat.id, '無效指令\n輸入 /start 查看全指令')
        car.check_message(message.chat.id, message.message_id, 5)
        car.log(update.message.chat.id, update.message.from_user.id,
                update.message.message_id, '無效指令 : %s' % (update.message.text))
    bot.deleteMessage(update.message.chat.id, update.message.message_id)


def new_chat_members(bot, update):
    for user in update.message.new_chat_members:
        if update.message.chat.id == Backup:
            bot.deleteMessage(update.message.chat.id,
                              update.message.message_id)
            if(car.point_vip_get(user.id)[0] > 0):
                bot.unban_chat_member(update.message.chat.id, user.id)
                car.log(update.message.chat.id, user.id,
                        update.message.message_id, '進入vip群不符合資格')
                car.vip_group_members(user.id, 0)
            else:
                car.vip_group_members(user.id, 1)
                car.log(update.message.chat.id, user.id,
                        update.message.message_id, '加入vip群')
        else:
            car.log(update.message.chat.id, user.id,
                    update.message.message_id, "新增成員")
        car.update_user(user.id, user.username,
                        user.last_name, user.first_name)


def left_chat_member(bot, update):
    car.update_user(update.message.left_chat_member.id, update.message.left_chat_member.username,
                    update.message.left_chat_member.last_name, update.message.left_chat_member.first_name)
    if update.message.chat.id == Backup:
        car.vip_group_members(update.message.left_chat_member.id, 0)
        car.log(update.message.chat.id, update.message.left_chat_member.id,
                update.message.message_id, '離開vip群')
    else:
        car.log(update.message.chat.id, update.message.left_chat_member.id,
                update.message.message_id, '離開了群組')


def sys_message(bot, update):
    car.log(update.message.chat.id, update.message.from_user.id,
            update.message.message_id, '系統訊息')


updater.dispatcher.add_handler(MessageHandler(
    Filters.status_update.new_chat_members, new_chat_members))
updater.dispatcher.add_handler(MessageHandler(
    Filters.status_update.left_chat_member, left_chat_member))
updater.dispatcher.add_handler(
    MessageHandler(Filters.status_update, sys_message))
updater.dispatcher.add_handler(MessageHandler(Filters.video, getVideo))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, getPhoto))
updater.dispatcher.add_handler(MessageHandler(Filters.document, getDocument))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, SetInstruction_processing))
updater.dispatcher.add_handler(MessageHandler(Filters.all, getmessage))
time.sleep(DELAY_TIME)
updater.start_polling()
updater.idle()
Open = False
t.join()
print('開始關閉')
car.stop()
