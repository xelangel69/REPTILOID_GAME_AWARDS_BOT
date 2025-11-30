from menu_methods import main_menu as m
import pandas as pd
import json
from data_methods import data_files as dfi, bot_info as bot


def delete_category(message):
    cat_to_delete = message.text
    if cat_to_delete == "↩️ Назад в Главное меню":
        bot.getBot().send_message(message.chat.id, "Отмена операции.", reply_markup=m.main_menu())
        return

    global categories
    if cat_to_delete in categories:
        categories.remove(cat_to_delete)
        with open(dfi.getCategoriesFile(), "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=4)

        # Удаляем все игры, связанные с этой категорией
        df = pd.read_excel(dfi.getDataFile())
        df = df[df["category"] != cat_to_delete]
        df.to_excel(dfi.getDataFile(), index=False)

        bot.getBot().send_message(message.chat.id, f"Категория '{cat_to_delete}' и все связанные игры удалены.",
                         reply_markup=m.main_menu())
    else:
        bot.getBot().send_message(message.chat.id, "Категория не найдена.", reply_markup=m.main_menu())