#!/usr/bin/python3
# TGBOT --> mysql 資料庫初始化
# 版本 : 3.1
import mysql.connector  # 引入 mysql API
import time
version = 3.1
################################################################
# 資料庫測試
DB = None
DB_cursor = None
Bot_id = None
Failure_Time = 0  # 連續發車時間
death_day = 7  # 死亡天數
death_message = 10  # 活躍值下限
message = []
LOG = []
car_Time = 0  # 車保存時間
restart_day = 0  # 系統資料還原時間
################################################################


def log(char_id, user_id, message_id, message, file_id=None):
    global LOG
    X=""
    if file_id != None:
        X = " : "
    else:
        file_id = ""

    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
          str(char_id).rjust(20), str(user_id).rjust(20), str(message),X,file_id)
    LOG.append([time.time(), char_id, user_id,
                message_id, str(message), Bot_id , file_id])
################################################################


def Start(bot_id, host, user, password, database):
    try:
        '初始化'
        global Failure_Time
        global DB
        global DB_cursor
        global DBup
        global DBup_cursor
        global car_Time
        global Bot_id
        global version
        global restart_day
        global death_message
        global death_day
        DB = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        DBup = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        Bot_id = bot_id
        # 啟用DB_cursor //發送指令物件
        DB_cursor = DB.cursor()
        DB_cursor.execute('SET NAMES utf8mb4')
        DB_cursor.execute("SET CHARACTER SET utf8mb4")
        DB_cursor.execute("SET character_set_connection=utf8mb4")
        # 啟用DBup_cursor //發送指令物件
        DBup_cursor = DBup.cursor()
        DBup_cursor.execute('SET NAMES utf8mb4')
        DBup_cursor.execute("SET CHARACTER SET utf8mb4")
        DBup_cursor.execute("SET character_set_connection=utf8mb4")
        # 創建variable 資料表
        SQL = 'CREATE TABLE IF NOT EXISTS variable(ID BIGINT(8) , Variable_name TEXT(256), VALUE_ TEXT(256))'
        DB_cursor.execute(SQL)
        # 創建car 資料表
        SQL = 'CREATE TABLE IF NOT EXISTS car(char_id BIGINT(8), USER_ID BIGINT(8), LOG_TIME DOUBLE(18,7))'
        DB_cursor.execute(SQL)
        # 創建 car_id 資料表
        SQL = 'CREATE TABLE IF NOT EXISTS car_id(char_id BIGINT(8), message_id BIGINT(8), LOG_TIME DOUBLE(18,7))'
        DB_cursor.execute(SQL)
        # 創建 log 資料表
        SQL = 'CREATE TABLE IF NOT EXISTS log(LOG_TIME DOUBLE(18,7), char_id BIGINT(8),Message_id  BIGINT(8), user_id BIGINT(8) , message TEXT(65535) , Bot_id BIGINT(4) , file_id TEXT(65535))'
        DB_cursor.execute(SQL)
        # 創建 User_Info 資料表
        SQL = 'CREATE TABLE IF NOT EXISTS User_Info(USER_ID BIGINT(8), USER_tag TEXT(256), USER_LIST TEXT(256) , USER_NAME TEXT(256))'
        DB_cursor.execute(SQL)
        # 創建 vip_group 資料表
        SQL = 'CREATE TABLE IF NOT EXISTS vip_group(USER_ID BIGINT(8), Day_activity BIGINT(8), countdown BIGINT(8) , member TINYINT(1))'
        DB_cursor.execute(SQL)
        SQL = 'CREATE TABLE IF NOT EXISTS blacklist(USER_ID BIGINT(8),Day DOUBLE(18,7))'
        DB_cursor.execute(SQL)
        SQL = 'CREATE TABLE IF NOT EXISTS Stock_car(ID int NOT NULL AUTO_INCREMENT,file_id TEXT(65535),type_ TINYINT(1),PRIMARY KEY(ID))'
        DB_cursor.execute(SQL)
        SQL = 'CREATE TABLE IF NOT EXISTS Activity_member(USER_ID BIGINT(8),LOG_TIME DOUBLE(18,7),Keywords TEXT(256))'
        DB_cursor.execute(SQL)
        # 發送指令
        DB.commit()
        DBup.commit()
        # 取得變數
        DB_cursor.execute("SELECT VALUE_ FROM variable")
        data = DB_cursor.fetchall()
        log(bot_id, 0, 1, "程序啟動 ID : " + str(bot_id) + "  版本 : " + str(version))
        try:
            car_Time = int(data[0][0])
            Failure_Time = int(data[1][0])
            death_message = int(data[4][0])
            death_day = int(data[5][0])
            restart_day = int(data[7][0])
            data[8][0]
        except:
            return False
    except:
        print("無法連接")
        time.sleep(5)
        data = Start(bot_id, host, user, password, database)
    print("OK")
    return data

# 註冊發車人


def start_car(char_id, user_id):
    '發車登記'
    try:
        global Failure_Time
        global DB
        global DB_cursor
        if not((type(char_id) == int) and (type(user_id) == int)):
            return False
        DB_cursor.execute(
            "SELECT * FROM car Where char_id=%s AND user_id=%s" % (str(char_id), str(user_id)))
        data = DB_cursor.fetchall()
        if len(data) != 0:
            DB_cursor.execute('UPDATE car SET LOG_TIME = %s WHERE char_id = %s AND user_id = %s' % (
                str(time.time()+Failure_Time), str(char_id), str(user_id)))
        else:
            SQL = 'INSERT INTO car(char_id,USER_ID,LOG_TIME) VALUES(%s,%s,\'%s\')' % (
                str(char_id), str(user_id), str(time.time()+Failure_Time))  # 新增紀錄
            DB_cursor.execute(SQL)
        DB.commit()
    except:
        return False
    return True


"""查詢駕照"""


def get_car_user(char_id, user_id):
    global DB_cursor
    try:
        DB_cursor.execute("SELECT * FROM car Where char_id=%s AND user_id=%s AND LOG_TIME >= %s" %
                          (str(char_id), str(user_id), str(time.time())))
        result = DB_cursor.fetchall()
        if len(result) != 0:
            return result[0][2]
        return 0
    except:
        return -1


def stop_car(char_id, user_id):
    '停止發車'
    try:
        global DB
        global DB_cursor
        if not((type(char_id) == int) and (type(user_id) == int)):
          return False
        if(char_id == 1):
          IF = " user_id = %s"%(user_id)
        else:
          IF = "char_id = %s AND user_id = %s"%(char_id,user_id)
        DB_cursor.execute(
            "SELECT * FROM car Where %s"%(IF))
        data = DB_cursor.fetchall()
        if len(data) != 0:
            DB_cursor.execute('UPDATE car SET LOG_TIME = "%s" WHERE %s' % (str(time.time()), IF))
            return True
        return False
    except:
        return -1

################################################################


def new_car(char_id, message_id):
    '發車登入'
    global message
    message.append((char_id, message_id, time.time()+car_Time))
    return True


def check_message(char_id, message_id, ntime):
    '發車登入'
    global message
    message.append((char_id, message_id, time.time()+ntime))
    return True


point_ = [None, None]
# 點數增加


def point(User_id):
    global point_
    if(User_id == None):
        return False
    if point_ != [None, None]:
        if User_id != point_[0]:
            point_update()
            point_[0] = User_id
            point_[1] = 1
        else:
            point_[1] += 1
    else:
        point_[0] = User_id
        point_[1] = 1
# 活躍值上傳
def point_Reset(User_id):
    try:
        global DB
        global DB_cursor
        DB_cursor.execute(
            "SELECT USER_ID FROM vip_group Where USER_ID=%s" % (str(User_id)))
        data = DB_cursor.fetchall()
        if len(data) != 0:
            DB_cursor.execute('UPDATE vip_group SET Day_activity= 0 , countdown = %s WHERE USER_ID = %s ' %
                              (str(death_day), str(User_id) ))
        else:
            SQL = 'INSERT INTO vip_group(USER_ID , Day_activity , countdown , member ) VALUES(%s,0,%s,0)' % (
                 str(User_id),str(death_day))
            DB_cursor.execute(SQL)
        DB.commit()
    except:
      return False
    return True

def point_update():
    try:
        global DB
        global DB_cursor
        global point_
        if(point_ == [None, None]):
            return False
        if point_[0] == None or point_[1] == None or point_[0] == 0 or point_[1] == 0:
            return False
        DB_cursor.execute(
            "SELECT * FROM vip_group Where USER_ID=%s" % (str(point_[0])))
        data = DB_cursor.fetchall()
        if len(data) != 0:
            DB_cursor.execute('UPDATE vip_group SET Day_activity= IF(Day_activity+ %s < 1000 , Day_activity + %s , 1000 ) WHERE USER_ID = %s ' %
                              (str(point_[1]), str(point_[1]), str(point_[0])))
        else:
            SQL = 'INSERT INTO vip_group(USER_ID , Day_activity , countdown , member ) VALUES(%s,%s,0,0)' % (
                str(point_[0]), str(point_[1]))
            DB_cursor.execute(SQL)
        DB.commit()
        point_ = [None, None]
    except:
        return False
    return True
# 點數進群資格查詢


def point_vip_get(user_id):
    point_update()
    try:
        DB_cursor.execute(
            "SELECT Day_activity , member FROM vip_group Where USER_ID=%s " % (user_id))
        result = DB_cursor.fetchall()
        return [death_message-result[0][0], result[0][1]]
    except:
        return [death_message, 0]
# 要刪除的用戶名單


def point_vip_members_delete():
    global restart_day
    global DB
    global DB_cursor

    tt = time.gmtime(time.time()+28800)
    if(tt.tm_hour == 0 and tt.tm_min == 0):
        if not(restart_day < tt.tm_mday):
            try:
                DB_cursor.execute("SELECT VALUE_ FROM variable Where ID = 7")
                data = DB_cursor.fetchall()
            except:
                return [False, -404]
            try:
                restart_day = int(data[0][0])
            except:
                return [False, -1]
            if not(restart_day < tt.tm_mday):
                return [False, -2]
    else:
        return [False, -2]
    point_update()
    try:

        DB_cursor.execute(
            'UPDATE vip_group SET countdown = countdown + 1 WHERE member = 1 AND Day_activity < %s ' % (death_message))
        DB_cursor.execute(
            'UPDATE vip_group SET countdown = 0 WHERE member = 1 AND Day_activity >= %s AND countdown> 0' % (death_message))
        DB_cursor.execute('UPDATE vip_group SET Day_activity = IF ( Day_activity-%s > 0 , Day_activity - %s , 0 ) WHERE 1' %
                          (death_message, death_message))
        DB_cursor.execute(
            "SELECT USER_ID FROM vip_group Where countdown>= %s AND member = 1" % (death_day+1))
        result = DB_cursor.fetchall()
        DB_cursor.execute(
            'UPDATE vip_group SET countdown = 0 WHERE countdown>= %s AND member = 1' % (death_day+1))
        DB_cursor.execute(
            'UPDATE variable SET VALUE_ = %s WHERE ID = 7' % (tt.tm_mday))
        DB_cursor.execute(
            "SELECT USER_ID , %s - countdown  FROM vip_group Where countdown>= %s AND member = 1" % (death_day, death_day-3))
        result_ = DB_cursor.fetchall()
        restart_day = tt.tm_mday
    except:
        return [False, -2]

    return [True, result, result_, tt.tm_mday]


def updata():
    """檢查上傳"""
    global message
    global DBup_cursor
    global DBup
    global LOG
    try:
        DBup_cursor.execute('select NOW()')
        DBup_cursor.fetchall()
    except:
        print("Error")
        return False

    if len(message) != 0:
        tt = 0
        for l in message:
            if l[2] < tt:
                tt = l[2]
        if len(message) >= 100 or (tt <= (time.time()+50)):
            sqlStuff = "INSERT INTO car_id (char_id, message_id , LOG_TIME) VALUES (%s,%s,%s)"
            DBup_cursor.executemany(sqlStuff, message)
            DBup.commit()
            message = []
    if len(LOG) != 0:
        if len(LOG) >= 10 or ((LOG[0][0]+60) <= time.time()):
            sqlStuff = "INSERT INTO log (log_time ,char_id,user_id,Message_id, message ,Bot_id ,file_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            DBup_cursor.executemany(sqlStuff, LOG)
            DBup.commit()
            LOG = []
    return True


# 檢查要刪除的車,檢查要上傳的
def delete_message():
    global DB_cursor
    global DB
    try:
        DB_cursor.execute(
            "SELECT * FROM car_id Where LOG_TIME<=%s " % (time.time()))
        result = DB_cursor.fetchall()
        sql = "DELETE FROM car_id WHERE Log_time <= %s" % (time.time())
        DB_cursor.execute(sql)
        DB.commit()
    except:
        return [False, []]
    if result:
        return [True, result]
    else:
        return [True, []]


def update_car():
    """更新檢查"""
    return updata()
# 用戶信息檢查更新


def update_user(USER_ID, USER_tag, USER_LIST, USER_NAME):
    try:
        global DB
        global DB_cursor
        DB_cursor.execute(
            "SELECT * FROM User_Info Where USER_ID=%s" % (str(USER_ID)))
        data = DB_cursor.fetchall()
        if len(data) != 0:
            DB_cursor.execute('UPDATE User_Info SET USER_tag = \'%s\' , USER_LIST = \'%s\' , USER_NAME = \'%s\' WHERE USER_ID = %s' % (
                str(USER_tag), str(USER_LIST), str(USER_NAME), str(USER_ID)))
        else:
            SQL = 'INSERT INTO User_Info(USER_ID , USER_tag , USER_LIST , USER_NAME ) VALUES(%s,\'%s\',\'%s\',\'%s\')' % (
                str(USER_ID), str(USER_tag), str(USER_LIST), str(USER_NAME))
            DB_cursor.execute(SQL)
        DB.commit()
    except:
        return False
    return True
# 更改vip群人員狀態


def vip_group_members(user_id, member):
    try:
        global DB
        global DB_cursor
        DB_cursor.execute(
            "SELECT * FROM vip_group Where USER_ID=%s" % (str(user_id)))
        data = DB_cursor.fetchall()
        if len(data) != 0:
            DB_cursor.execute('UPDATE vip_group SET member = %s WHERE USER_ID = %s' % (
                str(member), str(user_id)))
        else:
            SQL = 'INSERT INTO vip_group(USER_ID , Day_activity , countdown , member ) VALUES(%s,0,0,%s)' % (
                str(user_id), str(member))
            DB_cursor.execute(SQL)
        DB.commit()
    except:
        return False
    return True      

def blacklist(char_id):
    result = None
    try:
        global DB_cursor
        DB_cursor.execute(
            "SELECT Day FROM blacklist Where USER_ID = %s AND Day>=%s" % (char_id, time.time()))
        result = DB_cursor.fetchall()
    except:
        return -1
    if(not result):
        return None
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result[0][0]))

################################################################
def messageLookFor(chat_id,message_id):
    try:
        global DB_cursor
        DB_cursor.execute("SELECT user_id FROM log Where char_id = %s AND Message_id = %s"%(chat_id,message_id))
        result = DB_cursor.fetchall()
    except:
        return -1
    if(not result):
        return -2
    return result[0][0]

def blacklist_status(char_id, status, Day=None):
    try:
        global DB
        global DB_cursor
        if not((type(char_id) == int) and (type(status) == bool) and (type(Day) == int)):
            return False
        if(not status):
              Day = time.time()
        elif(Day == -1):
              Day = time.time()+1000000000
        else:
            Day *=86400
            Day += time.time()
        DB_cursor.execute(
            "SELECT Day FROM blacklist Where USER_ID=%s" % (str(char_id)))
        data = DB_cursor.fetchall()
        if len(data) != 0:
            DB_cursor.execute('UPDATE blacklist SET Day = %s WHERE USER_ID = %s' % (
                str(Day), str(char_id)))
        else:
            SQL = 'INSERT INTO blacklist(USER_ID,Day) VALUES(%s,%s)' % (
                str(char_id), str(Day))  # 新增紀錄
            DB_cursor.execute(SQL)
        DB.commit()
    except:
        return False
    return True
def get_car(user_id , Keywords):
    try:
        global DB
        global DB_cursor
        DB_cursor.execute(
            'SELECT LOG_TIME FROM Activity_member Where USER_ID = %s AND Keywords LIKE "%s"' % (str(user_id),Keywords))
        data = DB_cursor.fetchall()
        if len(data) != 0:
            return -2#已領取過此次活動
        DB_cursor.execute('SELECT * FROM Stock_car LIMIT 1')
        result = DB_cursor.fetchall()
        if(not result):
            return -3#已沒有車
        else :
            SQL = 'INSERT INTO Activity_member (USER_ID, LOG_TIME, Keywords) VALUES (%s , %s, "%s")'%(user_id,time.time(),Keywords)
            DB_cursor.execute(SQL)
            DB_cursor.execute('DELETE FROM Stock_car Where id = %s'%(result[0][0]))
            DB.commit()
    except:
        return -1#錯誤
    return result[0]#成功回傳file_id
def new_car_data(file_id , type_):
    global DB
    global DB_cursor
    if(file_id == None or type_ == None):
        log(0,0,0,'新增車數值為空file_id = %s type_ = %s'%(file_id , type_))
        return False
    try:
        SQL = 'INSERT INTO Stock_car (ID, file_id, type_) VALUES (NULL , "%s", %s)'%(str(file_id),str(type_))
        DB_cursor.execute(SQL)
        DB.commit()
    except:
        return False
    return True

def stop():
    '關閉'
    global message
    global DB_cursor
    global DB
    global LOG
    try:
        sqlStuff = "INSERT INTO car_id (char_id, message_id , LOG_TIME) VALUES (%s,%s,%s)"
        DB_cursor.executemany(sqlStuff, message)
        DB.commit()
        point_update()
        log(Bot_id, 0, 0, "系統ID : " + str(Bot_id) + " 已關閉")
        sqlStuff = "INSERT INTO log (log_time ,char_id,user_id, message ,Bot_id) VALUES (%s,%s,%s,%s,%s)"
        DB_cursor.executemany(sqlStuff, LOG)
        DB.commit()
    except:
        print('錯誤')
    # 關閉DB_cursor物件
    DB_cursor.close()
    # 關閉DB物件
    DB.close()
    print("關閉完成")
