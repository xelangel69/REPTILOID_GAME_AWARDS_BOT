from telebot import types
import pandas as pd
from data_methods import bot_info as bot, data_files as dfi
from menu_methods import main_menu as m

def show_games_for_vote(message):
    category = message.text
    if category == "↩️ Назад в Главное меню":
        bot.getBot().send_message(message.chat.id, "Отмена операции.", reply_markup=m.main_menu())
        return

    df = pd.read_excel(dfi.getDataFile())
    games = df[df["category"] == category]["game"].tolist()

    if not games:
        bot.getBot().send_message(message.chat.id, "В этой категории ещё нет игр.", reply_markup=m.main_menu())
        return

    markup = types.InlineKeyboardMarkup()
    for g in games:
        markup.add(types.InlineKeyboardButton(g, callback_data=f"vote|{category}|{g}"))

    bot.getBot().send_message(message.chat.id, "Нажмите на игру, за которую хотите проголосовать:", reply_markup=markup)
