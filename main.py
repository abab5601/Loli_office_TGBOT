import configparser
import logging

import telegram
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters

# 從config.ini文件加載數據
config = configparser.ConfigParser()
config.read('config.ini')

# 啟用日誌記錄
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# 最初的Flask應用程序
app = Flask(__name__)

# 通過Telegram訪問令牌的初始bot
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        
        # Update dispatcher process that handler to process this message
        # 更新調度程序進程處理此消息的處理程序
        dispatcher.process_update(update)
    return 'ok'


def reply_handler(bot, update):
    """Reply message."""
    if update.message.chat_id ==-1001278835291 :
        if update.message.video!=None:
            bot.send_video(-1001454460679,update.message.video)
        elif update.message.photo!=None:
            bot.send_photo(-1001454460679,update.message.photo)
        elif update.message.document!=None:
            bot.send_document(-1001454460679,update.message.document)
def NO_service(bot, update):
    bot.send_message(update.message.chat_id, "本機器人只服務羅咖office群")


# New a dispatcher for bot
# 新的機器人調度員
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
# 添加處理消息的處理程序，有很多種消息。 對於此處理程序，它特定處理文本消息。
whitelist=Filters.chat(-1001278835291)|Filters.chat(726651325)|Filters.chat(-397685471)
#                       羅咖                        開發者                      備份群
dispatcher.add_handler(MessageHandler(whitelist, reply_handler))
dispatcher.add_handler(MessageHandler(~whitelist, NO_service))

if __name__ == "__main__":
    # 運行服務器
    app.run(debug=True)
