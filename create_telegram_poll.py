from data_methods import bot_info as bot, data_files as dfi
import pandas as pd
from menu_methods import main_menu as m

def create_telegram_poll(message):
    category = message.text
    if category == "↩️ Назад в Главное меню":
        bot.getBot().send_message(message.chat.id, "Отмена операции.", reply_markup=m.main_menu())
        return

    df = pd.read_excel(dfi.getDataFile())
    category_df = df[df["category"] == category]
    games = category_df["game"].tolist()

    if len(games) < 2:
        bot.getBot().send_message(message.chat.id, "Нужно минимум две игры для создания опроса.", reply_markup=m.main_menu())
        return

    # Проверяем, был ли уже создан опрос для этой категории
    if category_df["poll_id"].astype(str).str.len().max() > 0:
        bot.getBot().send_message(message.chat.id, "Опрос для этой категории уже создан. Сначала удалите старый опрос.",
                         reply_markup=m.main_menu())
        return

    # Создаем опрос (poll)
    try:
        # poll_options не должен превышать 100 символов, но игры на английском, так что ОК
        poll_message = bot.getBot().send_poll(
            chat_id=message.chat.id,
            question=f"🏆 Категория: {category}",
            options=games,
            is_anonymous=False,  # Видим, кто за что голосует
            type='regular'  # Обычный опрос, не викторина
        )

        # Сохраняем ID опроса, чтобы знать, какой опрос соответствует категории
        poll_id = poll_message.poll.id

        # Обновляем DataFrame: добавляем poll_id ко всем играм этой категории
        df.loc[df["category"] == category, "poll_id"] = poll_id
        df.to_excel(dfi.getDataFile(), index=False)

        bot.getBot().send_message(message.chat.id, f"✅ Опрос для категории '{category}' успешно создан! ID опроса сохранен.",
                         reply_markup=m.main_menu())

    except Exception as e:
        bot.getBot().send_message(message.chat.id, f"❌ Ошибка при создании опроса (возможно, не чат/группа): {e}",
                         reply_markup=m.main_menu())
