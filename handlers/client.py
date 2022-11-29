from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.client_kb import kb_client
from keyboards.client_kb import start_client
from keyboards.client_kb import search_client
from config import START_MESSAGE as GREETINGS
from API_processing.proccessing import trending_process
from API_processing.proccessing import random_process
from API_processing.proccessing import get_gif_link
from API_processing.proccessing import rating_proccess
from API_processing.proccessing import get_response
from config import HELP


class FSMAdmin(StatesGroup):
    query = State()
    rating = State()
    repeat = State()


async def command_start(message: types.Message):
    await message.answer(GREETINGS, parse_mode="HTML", reply_markup=kb_client)


async def command_help(message: types.Message):
    await message.answer(HELP, parse_mode="HTML", reply_markup=kb_client)


async def random_gif(message: types.Message):
    link = await random_process()
    await message.answer_animation(link)


async def trending(message: types.Message):
    link = await trending_process()
    await message.answer_animation(link)


async def unknown_message(message: types.Message):
    await message.answer('Некорректная команда. Попробуйте воспользоваться кнопками из меню.', parse_mode="HTML", reply_markup=kb_client)


async def incorrect_format(message: types.Message):
    await message.answer('Некорректный формат данных. Попробуйте воспользоваться кнопками из меню.', parse_mode="HTML",
                         reply_markup=kb_client)


async def start_searching(message: types.Message):
    await FSMAdmin.query.set()
    await message.reply('Введите слово или фразу:', parse_mode="HTML", reply_markup=ReplyKeyboardRemove())


async def load_text_query(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['query'] = message.text[0:25]
    await FSMAdmin.next()
    await message.reply("Выберите уровень адекватности:", parse_mode="HTML", reply_markup=start_client)


async def load_amount_gifs(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['rating'] = await rating_proccess(message.text)
    async with state.proxy() as data:
        data['response'] = await get_response(data)
        link = await get_gif_link(data['response'])
    if link:
        await FSMAdmin.next()
        try:
            await message.answer_animation(link, reply_markup=search_client)
        except:
            await message.answer("Извините, что-то пошло не так... Попробуйте еще раз", parse_mode="HTML")
    else:
        await state.finish()
        await message.answer("К сожалению, ничего не найдено. Попробуйте другой запрос.", reply_markup=kb_client,
                             parse_mode="HTML")


async def more_gifs(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        link = await get_gif_link(data['response'])
    if link:
        try:
            await message.answer_animation(link)
        except:
            await message.answer("К сожалению, ничего не найдено. Попробуйте другой запрос.", reply_markup=kb_client,
                             parse_mode="HTML")
    else:
        await state.finish()
        await message.answer("По данному запросу больше ничего нет. Попробуйте что-нибудь новое!", reply_markup=kb_client,
                             parse_mode="HTML")


async def back_to_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберите действие из меню', reply_markup=kb_client)


async def cancel_searching(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Неизвестная команда. Возвращаемся в меню...', reply_markup=kb_client)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, content_types=types.ContentType.TEXT, commands=['start'])
    dp.register_message_handler(command_help, content_types=types.ContentType.TEXT, commands=['help'])
    dp.register_message_handler(random_gif, lambda message: 'Случайная GIF' in message.text)
    dp.register_message_handler(trending, lambda message: 'Популярные GIF' in message.text)
    dp.register_message_handler(start_searching, lambda message: 'Поиск по ключевым словам' in message.text, state=None)
    dp.register_message_handler(load_text_query, content_types=types.ContentType.TEXT, state=FSMAdmin.query)
    dp.register_message_handler(load_amount_gifs, content_types=types.ContentType.TEXT, state=FSMAdmin.rating)
    dp.register_message_handler(more_gifs, lambda message: 'Найти еще GIF' in message.text, state=FSMAdmin.repeat)
    dp.register_message_handler(back_to_menu, lambda message: 'Вернуться в меню' in message.text, state=FSMAdmin.repeat)
    dp.register_message_handler(cancel_searching, content_types=['photo', 'document', 'text'], state=FSMAdmin.repeat)
    dp.register_message_handler(unknown_message)
    dp.register_message_handler(incorrect_format, content_types=['photo', 'document'])

#Дописать выход из поиска и обработку неверного формата