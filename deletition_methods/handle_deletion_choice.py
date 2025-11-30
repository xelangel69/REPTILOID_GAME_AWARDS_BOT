from data_methods import bot_info as bot
import delete_poll_id
import choose_game_to_delete
import delete_category

def handle_deletion_choice(message):
    choice = message.text
    if choice == "↩️ Назад в Главное меню":
        bot.getBot().send_message(message.chat.id, "Отмена операции.", reply_markup=m.main_menu())
    elif choice == "Удалить Категорию":
        msg = bot.getBot().send_message(message.chat.id, "Выберите категорию для удаления:", reply_markup=c.category_menu())
        bot.getBot().register_next_step_handler(msg, delete_category)
    elif choice == "Удалить Игру":
        msg = bot.getBot().send_message(message.chat.id, "Выберите категорию, из которой хотите удалить игру:", reply_markup=c.category_menu())
        bot.getBot().register_next_step_handler(msg, choose_game_to_delete)
    elif choice == "Удалить Опрос":
        msg = bot.getBot().send_message(message.chat.id, "Выберите категорию, опрос которой нужно удалить (сбросить ID):", reply_markup=c.category_menu())
        bot.getBot().register_next_step_handler(msg, delete_poll_id)
    else:
        bot.getBot().send_message(message.chat.id, "Неверный выбор.", reply_markup=m.main_menu())