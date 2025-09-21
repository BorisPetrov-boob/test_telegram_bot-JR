from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def save_cancel_kb() -> InlineKeyboardMarkup:
    """Inline-кнопки для сохранения/отмены"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Сохранить как объявление", callback_data="save_text"),
                InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_text")
            ]
        ]
    )

