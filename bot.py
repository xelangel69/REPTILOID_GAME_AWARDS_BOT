import pandas as pd
import json
import os
from data_methods import data_files as df, bot_info as bot, export_data as ed
from menu_methods import category_menu as c, main_menu as m
from game_methods import ask_game_name as agn, show_games_for_vote as sgfv
import add_category as ac
import create_telegram_poll as ctp
from deletition_methods import deletion_menu as dm

# --- 🔑 ВАШ АКТУАЛЬНЫЙ ТОКЕН 🔑 ---
BOT_TOKEN = bot.getToken()
bot = bot.getBot()

# --- ИНИЦИАЛИЗАЦИЯ ДАННЫХ И ФАЙЛОВ ---
DATA_FILE = df.getDataFile()
CATEGORIES_FILE = df.getCategoriesFile()

# Убедимся, что DataFrame имеет нужные типы данных
initial_columns = ["user_id", "username", "category", "game", "votes", "poll_id"] 

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=initial_columns)
    df.to_excel(DATA_FILE, index=False)
    df = pd.read_excel(DATA_FILE) # Перезагружаем для использования

if not os.path.exists(CATEGORIES_FILE):
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
    with open(CATEGORIES_FILE, "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=4)

# Загружаем категории при запуске
with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
    categories = json.load(f)

# --- ОБРАБОТЧИКИ СООБЩЕНИЙ ---

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я REPTILOID_GAME_AWARDS_BOT 🦖", reply_markup=m.main_menu())

@bot.message_handler(func=lambda m: True)
def menu_handler(message):
    if message.text == "↩️ Назад в Главное меню":
        bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=m.main_menu())
    elif message.text == "Предложить категорию":
        msg = bot.send_message(message.chat.id, "Введите название новой категории (на русском):")
        bot.register_next_step_handler(msg, ac.add_category)
    elif message.text == "Предложить игру":
        msg = bot.send_message(message.chat.id, "Выберите категорию для игры:", reply_markup=c.category_menu())
        bot.register_next_step_handler(msg, agn.ask_game_name)
    elif message.text == "Голосовать":
        msg = bot.send_message(message.chat.id, "Выберите категорию для голосования:", reply_markup=c.category_menu())
        bot.register_next_step_handler(msg, sgfv.show_games_for_vote)
    # 🌟 Новая функция "Создать голосование"
    elif message.text == "Создать голосование":
        msg = bot.send_message(message.chat.id, "Выберите категорию для создания опроса:", reply_markup=c.category_menu())
        bot.register_next_step_handler(msg, ctp.create_telegram_poll)
    # 🌟 Новая функция "Удалить"
    elif message.text == "Удалить":
        dm.deletion_menu(message)
    elif message.text == "Экспорт данных":
        ed.export_data(message)
    else:
        bot.send_message(message.chat.id, "Выберите действие с клавиатуры.", reply_markup=m.main_menu())

@bot.callback_query_handler(func=lambda call: call.data.startswith("vote|"))
def handle_vote(call):
    _, category, game = call.data.split("|")
    df = pd.read_excel(DATA_FILE)
    
    try:
        idx = df[(df["game"] == game) & (df["category"] == category)].index[0]
    except IndexError:
        bot.answer_callback_query(call.id, "Ошибка: Игра не найдена.")
        return

    # Проверка, голосовал ли уже пользователь
    votes = df.at[idx, "votes"]
    votes_list = votes.split(",") if pd.notna(votes) and votes else []
    user_tag = str(call.from_user.id)
    
    if user_tag in votes_list:
        bot.answer_callback_query(call.id, "Вы уже голосовали за эту игру!")
        return
        
    votes_list.append(user_tag)
    df.at[idx, "votes"] = ",".join(votes_list)
    df.to_excel(DATA_FILE, index=False)
    
    bot.answer_callback_query(call.id, f"Вы проголосовали за '{game}'!")

# --- 🚨 ФУНКЦИЯ ДЛЯ ВЕБХУКА (ОБЯЗАТЕЛЬНА ДЛЯ PYTHONANYWHERE) 🚨 ---
def process_new_updates(update):
    """
    Обязательная функция для передачи обновлений от Flask в telebot.
    """
    bot.process_new_updates([update])