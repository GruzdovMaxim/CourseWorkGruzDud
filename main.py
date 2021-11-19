from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='2111621032:AAHOBL5KcOC8XjaRq34Nt1oREE-85G1UvBI')
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_mes(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Здраствуй!\nЯ - бот который может уведомлять тебя о вакансиях с "
                           "конкретных сайтов. Для большей информации, используй команду '/help'")


@dp.message_handler(commands='help')
async def help_mes(message: types.Message):
    sites = ["work.ua", "robota.ua"]
    all_commands = {"start": "Начало работы с ботом (автоматически выполняется в первый раз)",
                    "help": "Справка (включена в данный момент)",
                    "subscribe": "Подписка на какой-то сайт (есть опция выбрать все)",
                    "unsubscribe": "Отписка от какого-то сайта", }
    await bot.send_message(message.from_user.id,
                           "Бот обрабатывает такие сайты:" + "\n ".join(sites) +
                           "\nВсе команды для бота:\n " + "\n ".join(
                               [k + " - \n  " + all_commands[k] for k in all_commands.keys()]))


@dp.message_handler()
async def echo_answer(message: types.Message):
    await message.answer("ответ")


executor.start_polling(dp, skip_updates=True)
