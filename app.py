import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters

from db import db_requests, db_update
from database_queries import BotDB
from buttons.buttons import BUTTONS_PRODUCTS


bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = [
        "/Продал",
        "Компенсировал",
        "Нужно компенсировать",
        "Отчет",
        "/ALL"
        ]
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(*start_buttons)
    await message.answer("Что пожелаете?", reply_markup=buttons)


@dp.message_handler(commands="Продал")
async def get_sales_category(message: types.Message):
    category = await db_requests(BotDB.get_category())
    cat_list = []
    for category_tuple in category:
        for category_buttons in category_tuple:
            cat_list.append('/' + category_buttons)
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(*cat_list)
    await message.answer("Что продал?", reply_markup=buttons)


@dp.message_handler(commands=['Напитки', 'Кофе', 'Фреш', 'Лимонад', 'Чай'])
async def get_sales_prodycts(message: types.Message):
    products = await db_requests(
        BotDB.get_product(
            message.text.replace('/', '')
            )
        )
    response = []
    for products_tuple in products:
        for products_buttons in products_tuple:
            response.append('/' + products_buttons)
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(*response)
    await message.answer("Конкретнее", reply_markup=buttons)


@dp.message_handler(filters.Command(commands=BUTTONS_PRODUCTS))
async def sales_prodycts(message: types.Message):
    await db_requests(
        BotDB.update_quantity_product(
            message.text.replace('/', '')
        )
    )
    response = 'Еще'
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(response)
    await message.answer("Записал", reply_markup=buttons)


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
