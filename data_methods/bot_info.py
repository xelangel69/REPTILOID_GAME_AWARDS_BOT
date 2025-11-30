from telebot import *

BOT_TOKEN = "8413467526:AAHwY2YDRq5-bKvWW3FminyGmuPTZJ2eyVM"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

def getToken():
    return BOT_TOKEN

def getBot():
    return bot