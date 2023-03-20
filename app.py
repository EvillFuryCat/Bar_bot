import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from db import db_requests
from database_queries import BotDB
from commands.commands import (
    CHOICE_CATEGORY,
    DEBT,
    SALE_METHOD,
    START,
    CASHBOX,
    BUTTONS_PRODUCTS,
    START_BUTTONS,
    SALE_METHOD_BUTTONS,
)


bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class PaymentModes(StatesGroup):
    sale = State()


@dp.message_handler(commands=START, state="*")
async def start(message: types.Message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(*START_BUTTONS)
    await message.answer("Что пожелаете?", reply_markup=buttons)


@dp.message_handler(commands=CASHBOX, state="*")
async def choice_method_sales(message: types.Message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(*SALE_METHOD_BUTTONS)
    await message.answer("Выберете метод продажи", reply_markup=buttons)
    await PaymentModes.sale.set()


@dp.message_handler(commands=SALE_METHOD, state=PaymentModes.sale)
async def choice_category(message: types.Message, state: FSMContext):
    await state.update_data(sale_methood=message.text)
    category = await db_requests(BotDB.get_category())
    cat_list = []
    for category_tuple in category:
        for category_buttons in category_tuple:
            cat_list.append("/" + category_buttons)
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(*cat_list)
    await message.answer("Выберете категорию", reply_markup=buttons)


@dp.message_handler(commands=CHOICE_CATEGORY, state="*")
async def choice_prodycts(message: types.Message):
    products = await db_requests(BotDB.get_product(message.text.replace("/", "")))
    response = []
    for products_tuple in products:
        for products_buttons in products_tuple:
            response.append("/" + products_buttons)
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(*response)
    await message.answer("Выберете продукт", reply_markup=buttons)


@dp.message_handler(filters.Command(commands=BUTTONS_PRODUCTS), state="*")
async def choose_how_to_sell(message: types.Message, state: FSMContext):
    data_state = await state.get_data()
    if data_state["sale_methood"] == "/Продажа":
        await db_requests(BotDB.add_quantity_product(message.text.replace("/", "")))
        await message.answer("Продажа учтена")
    if data_state["sale_methood"] == "/Синхронизация":
        await db_requests(BotDB.reduce_quantity_product(message.text.replace("/", "")))
        await message.answer("Синхронизация учтена")


@dp.message_handler(commands=DEBT, state="*")
async def get_debt(message: types.Message):
    response_list = await db_requests(BotDB.get_debt())
    await message.answer(f"{response_list}")


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
