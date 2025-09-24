import asyncio
import json
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from config import TOKEN
from keyboards.reply import main_menu
from keyboards.inline import save_cancel_kb

import logging

bot = Bot(TOKEN)  # Создаем бота
dp = Dispatcher()  # Создаем диспетчер


@dp.message(Command('start'))  # Хэндлер на команду старт (5)
async def start_handler(message: Message):
    welcome_text = "Привет! Я бот для создания и управления объявлениями. Вот что я могу:\n\n" \
                   "/start - Показать это приветственное сообщение\n" \
                   "/help - Краткая инструкция по использованию бота\n" \
                   "/add - Создать новое объявление\n" \
                   "/list - Показать все сохраненные объявления\n\n" \

    await message.answer(welcome_text, reply_markup=main_menu())


@dp.message(Command('help'))  # Хэндлер на команду инфо (6) inline клавиатура
async def help_handler(message: Message):
    help_text = (
        "📖 Инструкция по использованию:\n\n"
        "1. /add - создать новое объявление\n"
        "2. /list - посмотреть все объявления\n\n"
    )
    await message.answer(help_text)


ADS_FILE = "ads.json"


def load_ads():
    try:
        with open(ADS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_ads(ads):
    try:
        with open(ADS_FILE, "w", encoding="utf-8") as f:
            json.dump(ads, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Ошибка сохранения файла: {e}")


@dp.message(Command("list"))
async def show_list(message: Message):
    """Показываем количество объявлений"""
    ads = load_ads()
    await message.answer(f"📋 Всего объявлений: {len(ads)}")


@dp.message()
async def message_handler(message: Message):
    """Обрабатываем входящие сообщения для создания объявлений"""
    ads = load_ads()
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name

    await message.answer("Меню", reply_markup=save_cancel_kb())
    await asyncio.sleep(2)
    if message.text and not message.text.startswith('/'):
        # Текстовое объявление
        new_ad = {
            "id": len(ads) + 1,
            "type": "text",
            "content": message.text,
            "user_id": user_id,
            "user": username
        }

        ads.append(new_ad)
        save_ads(ads)
        await message.answer("✅ Ваше текстовое объявление сохранено!")

    elif message.photo:
        # Фото объявление
        photo = message.photo[-1]
        new_ad = {
            "id": len(ads) + 1,
            "type": "photo",
            "file_id": photo.file_id,
            "user_id": user_id,
            "user": username
        }
        ads.append(new_ad)
        save_ads(ads)
        await message.answer("✅ Фото объявление сохранено!")

    elif message.audio:
        # Аудио объявление
        audio = message.audio
        new_ad = {
            "id": len(ads) + 1,
            "type": "audio",
            "file_id": audio.file_id,
            "user_id": user_id,
            "user": username
        }
        ads.append(new_ad)
        save_ads(ads)
        await message.answer("✅ Аудио объявление сохранено!")

    else:
        await message.answer("❌ Пожалуйста, отправьте текст, фото или аудио для объявления.")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())