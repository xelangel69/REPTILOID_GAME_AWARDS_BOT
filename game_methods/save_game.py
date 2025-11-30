from menu_methods import main_menu as m
from data_methods import bot_info as bot, data_files as dfi
import validations as val
import pandas as pd

def save_game(message, category):
    game = message.text.strip()
    if game == "↩️ Назад в Главное меню":
        bot.getBot().send_message(message.chat.id, "Отмена операции.", reply_markup=m.main_menu())
        return

    if not val.is_english(game) and not val.is_russian(game):
        bot.getBot().send_message(message.chat.id, "Название некорректно.", reply_markup=m.main_menu())
        return

    df = pd.read_excel(dfi.getDataFile())
    if ((df["game"] == game) & (df["category"] == category)).any():
        bot.send_message(message.chat.id, "Эта игра уже предложена.", reply_markup=m.main_menu())
        return

    new_row = pd.DataFrame([{
        "user_id": message.from_user.id,
        "username": message.from_user.username or message.from_user.first_name,
        "category": category,
        "game": game,
        "votes": "",
        "poll_id": ""  # Добавляем пустую колонку poll_id
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(dfi.getDataFile(), index=False)
    bot.getBot().send_message(message.chat.id, f"Игра '{game}' добавлена в категорию '{category}'!", reply_markup=m.main_menu())
