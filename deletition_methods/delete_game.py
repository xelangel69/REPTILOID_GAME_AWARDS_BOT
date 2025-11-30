import pandas as pd
from menu_methods import main_menu as m
from data_methods import data_files as dfi, bot_info as bot


def delete_game(message, category):
    game_to_delete = message.text
    if game_to_delete == "↩️ Назад в Главное меню":
        bot.getBot().send_message(message.chat.id, "Отмена операции.", reply_markup=m.main_menu())
        return

    df = pd.read_excel(dfi.getDataFile())
    # Ищем индекс строки с игрой и категорией
    idx_list = df[(df["game"] == game_to_delete) & (df["category"] == category)].index

    if not idx_list.empty:
        df = df.drop(idx_list)
        df.to_excel(dfi.getDataFile(), index=False)
        bot.getBot().send_message(message.chat.id, f"Игра '{game_to_delete}' из категории '{category}' удалена.",
                         reply_markup=m.main_menu())
    else:
        bot.getBot().send_message(message.chat.id, "Игра не найдена.", reply_markup=m.main_menu())