from data_methods import bot_info as bot
import handle_deletion_choice
from telebot import *

def deletion_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Удалить Категорию", "Удалить Игру")
    markup.add("Удалить Опрос", "↩️ Назад в Главное меню")
    bot.getBot().send_message(message.chat.id, "Что вы хотите удалить?", reply_markup=markup)
    bot.getBot().register_next_step_handler(message, handle_deletion_choice)