from telebot import *

def main_menu():
    """Главное меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Голосовать", "Создать голосование")
    markup.add("Предложить игру", "Предложить категорию")
    markup.add("Удалить", "Экспорт данных")
    return markup