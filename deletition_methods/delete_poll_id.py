import pandas as pd
from data_methods import data_files as dfi, bot_info as bot
from menu_methods import main_menu as m


def delete_poll_id(message):
    category = message.text
    if category == "↩️ Назад в Главное меню":
        bot.getBot().send_message(message.chat.id, "Отмена операции.", reply_markup=m.main_menu())
        return

    df = pd.read_excel(dfi.getDataFile())

    if df[df["category"] == category]["poll_id"].astype(str).str.len().max() > 0:
        df.loc[df["category"] == category, "poll_id"] = ""
        df.to_excel(dfi.getDataFile(), index=False)
        bot.getBot().send_message(message.chat.id, f"ID опроса для категории '{category}' сброшен. Вы можете создать новый опрос.", reply_markup=m.main_menu())
    else:
        bot.getBot().send_message(message.chat.id, f"Опрос для категории '{category}' не был создан.", eply_markup=m.main_menu())
