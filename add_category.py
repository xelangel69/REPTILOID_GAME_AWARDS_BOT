from menu_methods import main_menu as m
from data_methods import bot_info as bot


def add_category(message):
    new_cat = message.text.strip()
    if new_cat == "↩️ Назад в Главное меню":
        bot.getBot().send_message(message.chat.id, "Отмена операции.", reply_markup=m.main_menu())
        return

    global categories  # Необходимо для изменения глобальной переменной
    if new_cat not in categories:
        categories.append(new_cat)
        with open(CATEGORIES_FILE, "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=4)
        bot.getBot().send_message(message.chat.id, f"Категория '{new_cat}' добавлена!", reply_markup=m.main_menu())
    else:
        bot.getBot().send_message(message.chat.id, "Такая категория уже есть.", reply_markup=m.main_menu())