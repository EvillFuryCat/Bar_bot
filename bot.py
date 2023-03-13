import os

from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Продал", "Компенсировал", "Нужно компенсировать", "Отчет"]
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(*start_buttons)
    await message.answer("Что пожелаете?", reply_markup=buttons)


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
