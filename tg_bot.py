# Главный файл запуска бота
import asyncio
import logging
import re
import sqlite3
from datetime import datetime
from random import shuffle
from sqlite3 import connect
import magic_filter

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

import config

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
cb_data = CallbackData("fabnum", "action", "variaty", "category")
EMPTY_KB = ReplyKeyboardMarkup(resize_keyboard=True)


class Form(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()


class RegisterForm(StatesGroup):
    reg = State()


class SetCurrencyForm(StatesGroup):
    st = State()


# Initialize bot with using local server

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def main_bot():
    await dp.start_polling(bot)


@dp.message_handler(content_types=['contact'])
async def message_contact_handler(message: types.Message):
    # TODO: регистрация пользователей
    dct = message.contact
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    tg_id = dct.user_id
    name = dct.full_name
    phone = dct.phone_number
    result = 0

    phones = cur.execute(f"SELECT phone_number FROM USERS").fetchall()

    if (phone,) in phones:
        cur.execute(f"UPDATE USERS SET tg_id={tg_id} WHERE phone_number='{phone}'").fetchall()

    else:
        cur.execute(f"INSERT INTO USERS VALUES ({0}, {tg_id}, '{name}','{phone}',{0}, {0}, {0}, '')").fetchall()
    con.commit()

    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(types.InlineKeyboardButton("Записаться", web_app=types.WebAppInfo(url="https://wink.ru/media_items/149594267")))


    kb.add(types.InlineKeyboardButton(text="Пройти викторину",
                                      callback_data=cb_data.new(action="quiz", variaty="Пин-код", category=0)))
    await message.reply('Успех', reply_markup=kb)


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    print(message.from_user.id)
    kb = types.InlineKeyboardMarkup(row_width=3)

    kb.add(types.InlineKeyboardButton(text="Пин-код",
                                      callback_data=cb_data.new(action="try", variaty="Пин-код", category=0)))
    kb.add(types.InlineKeyboardButton(text="Чебурашка",
                                      callback_data=cb_data.new(action="try", variaty="Чебурашка", category=0)))
    kb.add(types.InlineKeyboardButton(text="Зеленая Книга",
                                      callback_data=cb_data.new(action="try", variaty="Зеленая Книга", category=0)))

    await message.reply("Привет!\nУгадай фрагмент из фильма и получи 60 дней подписки!\n")
    await message.reply_photo(open('1.jpg', 'rb'), reply_markup=kb)


@dp.callback_query_handler(cb_data.filter(action=["try"]))
async def add(call: types.CallbackQuery, callback_data: dict):
    kb = types.InlineKeyboardMarkup()
    otm = types.InlineKeyboardButton('Отправить свой контакт ☎️', request_contact=True,
                                     callback_data=cb_data.new(action="quest", variaty='', category=0))
    kb.add(otm)
    answer = ''
    if callback_data['variaty'] == 'Чебурашка':
        answer += 'Правильно!\n'
    else:
        answer += 'К сожалению, неверно'
    answer += "(Текст про конкурс)"
    markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
    )

    await call.message.reply(answer + '\nhttps://disk.yandex.ru/i/rNPUR_4h1rvFyA')
    await call.message.reply("Вам потребуется указать свой номер телефона для честности конкурса",
                             reply_markup=markup_request)
    await call.answer()


@dp.callback_query_handler(cb_data.filter(action=["quiz"]))
async def expenditure(call: types.CallbackQuery, callback_data: dict):
    try:
        con = sqlite3.connect('questions.db')
        cur = con.cursor()
        con_2 = sqlite3.connect('users.db')
        answered = con_2.cursor().execute(
            f"SELECT answered_questions FROM USERS WHERE tg_id={call.message.chat.id}").fetchone()[0]

        answered = [int(x) for x in answered.split()]
        print(answered)
        questions = cur.execute(f"SELECT * FROM Questions").fetchall()
        questions = [x for x in questions if x[0] not in answered]
        shuffle(questions)
        quest = questions[0]
        ids, quest, type_of_media, name_of_media, variants, right_variant, name_of_film, description, link = quest
        con_2.cursor().execute(f'UPDATE users SET current={ids} WHERE tg_id={call.message.chat.id}')
        con_2.commit()
        kb = ReplyKeyboardMarkup()
        for el in variants.split(';'):
            kb.add(KeyboardButton(el))

        await call.message.reply(quest, reply_markup=kb)
        try:
            if type_of_media == 'video':
                await call.message.answer_video(open('pictures' + '/' + name_of_media, 'rb'))
            elif type_of_media == 'picture':
                await call.message.answer_photo(open('pictures' + '/' + name_of_media, 'rb'))
            elif type_of_media == 'music':
                await call.message.answer_audio(open('pictures' + '/' + name_of_media, 'rb'))
        except Exception as e:
            print(e)
        await call.answer()
    except Exception as e:
        print(e)


@dp.message_handler()
async def send_message(message: types.Message):
    print(298437)
    try:
        con_user = sqlite3.connect('users.db')
        cur_user = con_user.cursor()
        current = cur_user.execute(f"SELECT current FROM USERS WHERE tg_id={message.chat.id}").fetchall()
        con_quest = sqlite3.connect('questions.db')
        cur_quest = con_quest.cursor()
        question = cur_quest.execute(f"SELECT correct_answer FROM questions WHERE id={current[0][0]}").fetchall()
    except Exception as e:
        print(e)
    if question[5] == message.text:
        print("ДА")
    else:
        print('НЕТ')
    await message.reply("Hi there!")


if __name__ == '__main__':
    asyncio.run(main_bot())
