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



bot = Bot(TOKEN) #Создаем бота
dp = Dispatcher() #Создаем диспетчер

AUDIO_JSON_FILE="audio.json"
PHOTOS_JSON_FILE = "photos.json"
TEXT_JSON_FILE = "texts.json"


class PhotoState(StatesGroup):
    waiting_for_description = State()

class TextState(StatesGroup):
    waiting_for_confirmatio = State()




@dp.message(Command('start')) #Хэндлер на команду старт (5)
async def start_handler(message: Message):
    welcome_text = "Привет! Я бот для создания и управления объявлениями. Вот что я могу:\n\n" \
                   "/start - Показать это приветственное сообщение\n" \
                   "/help - Краткая инструкция по использованию бота\n" \
                   "/add - Создать новое объявление\n" \
                   "/list - Показать все сохраненные объявления\n\n" \

    await message.answer(welcome_text, reply_markup=main_menu())



@dp.message(Command('help'))#Хэндлер на команду инфо (6) inline клавиатура
async def help_handler(message: Message):
    help_text = (
            "📖 Инструкция по использованию:\n\n"
            "1. /add - создать новое объявление\n"
            "2. /list - посмотреть все объявления\n\n"
    )
    await message.answer(help_text)



@dp.message(F.text & ~F.command)
async def text_handler(message: Message):
    text = message.text

    await message.answer("Хотите сохранить это как объявление?", reply_markup=save_cancel_kb())

    data = await state.get_data()
    file_id = data.get('file_id')
    await state.update_data(file_id=file_id)

@dp.callback_query(F.data == "save_text")
async def save_text_callback(callback: CallbackQuery, state: FSMContext):
    text_data = {
        "text": text_to_save,
        "user_id": callback.from_user.id,
        "username": callback.from_user.username,
        "first_name": callback.from_user.first_name,
        "message_id": callback.message.message_id,
        "date": callback.message.date.isoformat()
    }


    all_texts = load_texts()
    all_texts.append(text_data)
    save_texts(all_texts)



@dp.message(F.photo)
async def photo_handler(message: Message, state: FSMContext):
    photo = message.photo
    file_id = photo.file_id

    await message.answer("Добавить описание?")


    data = await state.get_data()
    file_id = data.get('file_id')

    photo_data = {
        "file_id": file_id,
        "description": None,
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "timestamp": message.date.isoformat(),
        "type": "photo"
    }

    # Сохраняем в JSON
    all_data = load_data(PHOTOS_JSON_FILE)
    all_data.append(photo_data)
    save_data(all_data, PHOTOS_JSON_FILE)

    await message.answer("Фото сохранено без описания!")



@dp.message(F.audio)#Хэндлер на аудио (9)
async def audio_handler(message: Message):
    audio = message.audio
    file_id = audio.file_id
    await message.answer('Аудио-объявление добавлено')

    audio_data = {
        "file_id": file_id,
        "file_name": audio.file_name,
        "duration": audio.duration,
        "mime_type": audio.mime_type,
        "file_size": audio.file_size,
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "timestamp": message.date.isoformat(),
        "type": "audio"
    }

    all_data = load_data(AUDIO_JSON_FILE)
    all_data.append(audio_data)
    save_data(all_data, AUDIO_JSON_FILE)

    await message.answer("Аудио-объявление добавлено!")







async def main(): #точка входа (1)
    logging.basicConfig(level=logging.INFO) #Логирование (2)
    await dp.start_polling(bot) #Запускаем поллинг (4)

asyncio.run(main())

