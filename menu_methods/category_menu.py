from telebot import types
import json
from data_methods import data_files as dfi
import os
import pandas as pd

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

def category_menu():
    """Меню выбора категорий с кнопкой 'Назад'"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for cat in categories:
        markup.add(cat)
    # 🌟 Добавлена кнопка "Назад"
    markup.add("↩️ Назад в Главное меню")
    return markup