from aiogram import Bot
from config import NOTIFY_CHAT_ID


async def send_notification(bot: Bot, data: dict, survey_id: int):
    if not NOTIFY_CHAT_ID:
        return

    actions = ", ".join(data.get("actions_taken", []))
    debtor_info = ", ".join(data.get("debtor_data", []))
    other_text = f"\n   Иное: {data.get('actions_other')}" if data.get("actions_other") else ""

    text = (
        f"\U0001f4cb Новая анкета #{survey_id}\n"
        f"{'=' * 30}\n"
        f"1. Роль: {data['role']}\n"
        f"2. Имя: {data['name']}\n"
        f"3. Член товарищества: {'Да' if data['is_member'] else 'Нет'}\n"
        f"4. Единственный собственник: {'Да' if data['is_sole_owner'] else 'Нет'}\n"
        f"5. Период долга: {data['debt_period']}\n"
        f"6. Сумма долга: {data['debt_amount']}\n"
        f"7. Действия: {actions}{other_text}\n"
        f"8. Письменные ответы должника: {'Да' if data['has_written_response'] else 'Нет'}\n"
        f"9. Данные на должника: {debtor_info}\n"
        f"10. Телефон: {data['contact_phone']}\n"
        f"{'=' * 30}\n"
        f"Telegram: @{data.get('telegram_username') or 'нет username'}"
    )

    await bot.send_message(chat_id=NOTIFY_CHAT_ID, text=text)
