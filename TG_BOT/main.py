from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging


class Reg(StatesGroup):
    typs = State()


texts_for_keyboards = [["Трасса ВЛ", "Крепления опоры, стойки, траверсы, крюка, изолятора на стойке опоры, провода",
                        "Приставка, стойка, подкос", "Траверса, крюк, изолятор на траверсе",
                        "Провод, кабельная вставка",
                        "Заземляющее устройство", "Коммутационные аппараты, разрядники"],
                       ["Площадка ТП", "Крепления, заделка в фунте, уплотнения", "Строительная часть",
                        "Распределительное устройство ВН (УВН 6-20 кВ, РУ 6-20 кВ)",
                        "Силовой трансформатор", "Распределительное устройство НН (РУНН 0,4 кВ, РУ 0,4 кВ)",
                        "Заземляющее устройство"],
                       ["Трасса ВЛ", "Крепление опоры, стойки, траверсы, крюка, изолятора, провода",
                        "Приставка, стойка, подкос", "Траверса, крюк, изолятор",
                        "Провод, кабельная вставка, ответвление от ВЛ к вводу в здание", "Заземляющее устройство",
                        "Разрядники, уличное освещение"]
                       ]
keyboards = []
for index_of_keyboard, _ in enumerate(texts_for_keyboards):
    keyboards.append(InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text_for_button, callback_data=f'k{index_of_keyboard}_b{index_of_button}')]
            for index_of_button, text_for_button in enumerate(texts_for_keyboards[index_of_keyboard])]))

BOT_TOKEN = '6337015878:AAGhMlZi0qe3S43_K0crcIsni9l_KUlib-E'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

chat_id = -4228585515
list_of_text = ["ВЛ 6 – 20 кВ", "ТП 6-20/0,4 кВ, РП 6-20 кВ", "ВЛ 0,38 кВ"]


@dp.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    logging.info(f"команда старт от {message.from_user.username}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=text)]
                                                     for text in list_of_text])
    await state.set_state(Reg.typs)
    await message.answer(text='Выберите объект:', reply_markup=keyboard)


@dp.callback_query(F.data.in_(list_of_text))
async def zxc(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Сфотографируйте неиcправность на объекте")
    for text in list_of_text:
        if callback.data == text:
            await state.update_data(typs=text)


@dp.message()
async def qwe(message: Message, state: FSMContext):
    if message.photo is not None:
        data = await state.get_data()
        data = data['typs']
        await bot.send_message(chat_id, f'Пришла фотография с объекта {data}')
        for index_of_keyboard, text in enumerate(list_of_text):
            if data == text:
                await bot.send_photo(chat_id=chat_id,
                                     photo=message.photo[-1].file_id,
                                     reply_markup=keyboards[index_of_keyboard])
        await state.clear()


import asyncio

if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    dp.run_polling(bot)
