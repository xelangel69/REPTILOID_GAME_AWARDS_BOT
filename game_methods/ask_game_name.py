from data_methods import bot_info as bot, data_files as dfi
from menu_methods import main_menu as m
import save_game as sg
import os
import json

initial_columns = ["user_id", "username", "category", "game", "votes", "poll_id"]

if not os.path.exists(dfi.getDataFile()):
    df = pd.DataFrame(columns=initial_columns)
    df.to_excel(dfi.getDataFile(), index=False)
    df = pd.read_excel(dfi.getDataFile()) # Перезагружаем для использования

if not os.path.exists(dfi.getCategoriesFile()):
    categories = [
        "Лучшая игра 2025 года",
        "Лучшее РПГ 2025 года",
        "Лучшая Action-Adventure 2025 года",
        "Лучшее DLC 2025 года",
        "Лучший шутер 2025 года",
        "Худшая игра 2025 года",
        "Лучший сюжет в играх 2025 года",
        "Лучшая инди игра 2025 года"
    ]
    with open(dfi.getCategoriesFile(), "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=4)

# Загружаем категории при запуске
with open(dfi.getCategoriesFile(), "r", encoding="utf-8") as f:
    categories = json.load(f)

def ask_game_name(message):
    category = message.text
    if category == "↩️ Назад в Главное меню":
        bot.getBot().send_message(message.chat.id, "Отмена операции.", reply_markup=m.main_menu())
        return

    if category not in categories:
        bot.getBot().send_message(message.chat.id, "Неверная категория.", reply_markup=m.main_menu())
        return
    msg = bot.getBot().send_message(message.chat.id, f"Введите название игры на английском для категории '{category}':")
    bot.getBot().register_next_step_handler(msg, sg.save_game, category)
