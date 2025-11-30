import pandas as pd
from menu_methods import main_menu as m
from data_methods import bot_info as bot


def export_data(message, data_file, document):
    df = pd.read_excel(data_file)

    # XLSX
    df.to_excel("export.xlsx", index=False)

    # DOCX
    doc = document()
    doc.add_heading("REPTILOID GAME AWARDS DATA", 0)
    for category in df["category"].unique():
        doc.add_heading(category, level=1)

        # Считаем количество голосов
        def count_votes(votes_str):
            if pd.isna(votes_str) or votes_str == "":
                return 0
            return len(str(votes_str).split(','))

        category_df = df[df["category"] == category].copy()
        category_df['vote_count'] = category_df['votes'].apply(count_votes)
        category_df = category_df.sort_values(by="vote_count", ascending=False)

        for _, row in category_df.iterrows():
            doc.add_paragraph(f"Игра: {row['game']} | Предложена: {row['username']} | Голосов: {row['vote_count']}")

    doc.save("export.docx")

    bot.getBot().send_message(message.chat.id, "Данные экспортированы: export.xlsx и export.docx.", reply_markup=m.main_menu())
