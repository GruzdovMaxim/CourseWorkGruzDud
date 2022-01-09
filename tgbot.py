import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from config import TOKEN

import codecs
import json
import markup as menu
import async_rabota_ua
import async_work_ua
import DB_worker

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

closeMenu = types.ReplyKeyboardRemove()

# all_vac = async_work_ua.get_all_vacancies("Python Developer", "Харьков", "Удаленная работа")

main_all_vac = []
counter = 0
main_user_id = 0
main_search_words = ""
parsing_finished = False


def show_vacancies(arg_counter):
    arg_counter * 5


class SearchVacs(StatesGroup):
    srch = State()


class ChangeCity(StatesGroup):
    city = State()


class ChangeEmp(StatesGroup):
    emp = State()


# def city_check(temp_var):
#     async_work_ua.get_all_vacancies("Python Developer", "Харьков", "Удаленная работа")
#     # temp_var = temp_var.lower().title()
#     # with codecs.open("all_city_names.json", "r", encoding='utf-8') as data_file:
#     #     data = json.load(data_file)
#     #     if temp_var in data.keys() or temp_var in data.values():
#     #         return True
#     # return False


@dp.message_handler(commands='start')
async def start_mes(message: types.Message):
    DB_worker.create_db_and_table(DB_worker.name_bd)
    DB_worker.delete_data(DB_worker.name_bd)
    DB_worker.save_data(DB_worker.name_bd, message.from_user.id)
    global main_user_id
    main_user_id = message.from_user.id
    await bot.send_message(message.from_user.id, f"Здраствуй, {message.from_user.first_name}!\n"
                                                 "Если ты обратился к нашему боту, значит ты хочешь искать важную информацию "
                                                 "быстро качественно. Наш бот поможет тебе: "
                                                 "Искать все вакансии сразу и выдавать это в удобном формате (к тому же со всех сайтов, с которыми бот имеет дело)"
                                                 "Искать по конкретными критериям (город, занятость) которые можно поменять или вовсе не указывать",
                           reply_markup=menu.mainMenu)


@dp.message_handler()
async def bot_mes(message: types.Message):
    if message.text == "🔎Поиск работы🔎":
        await SearchVacs.srch.set()
        await bot.send_message(message.from_user.id, "Введите ключевые слова", reply_markup=closeMenu)
    elif message.text == "💬Показать еще 10💬":
        global counter
        print(counter)
        await bot.send_message(message.from_user.id, "Сайт rabota.ua", reply_markup=menu.Search)
        if (counter + 1) * 5 < len(main_all_vac[0]):
            for temp in main_all_vac[0][counter * 5:(counter + 1) * 5]:
                await bot.send_message(message.from_user.id, temp, reply_markup=menu.Search)
        elif (counter + 1) * 5 > len(main_all_vac[0]) > counter * 5:
            for temp in main_all_vac[0][counter * 5:]:
                await bot.send_message(message.from_user.id, temp, reply_markup=menu.Search)
        else:
            await bot.send_message(message.from_user.id, "Вакансий больше нет (rabota.ua)", reply_markup=menu.Search)

        await bot.send_message(message.from_user.id, "Сайт www.work.ua", reply_markup=menu.Search)
        if (counter + 1) * 5 < len(main_all_vac[1]):
            for temp in main_all_vac[1][counter * 5:(counter + 1) * 5]:
                await bot.send_message(message.from_user.id, temp, reply_markup=menu.Search)
        elif (counter + 1) * 5 > len(main_all_vac[1]) > counter * 5:
            for temp in main_all_vac[1][counter * 5:]:
                await bot.send_message(message.from_user.id, temp, reply_markup=menu.Search)
        else:
            await bot.send_message(message.from_user.id, "Вакансий больше нет (work.ua)", reply_markup=menu.Search)
        counter += 1

    elif message.text == "📃Помощь📃":
        await bot.send_message(message.from_user.id,
                               "Наш бот использует асинхронный парсинг и был написан на ЯП Python. "
                               "Бот пока что обрабатывает всего два сайта, но уже делает это быстро и довольно качественно."
                               "После нажатия кнопки \"искать\" бот сразу парсит данные и находит все вакансии на всех сайтах."
                               "Важно заметить что не смотря на быструю обработку (асинхронный процес), парсинг может занять вообщем "
                               "по времени от 2-3 секунд до 8 (что случается довольно редко, чаще всего 3-4 секунды)",
                               reply_markup=menu.mainMenu)

    elif message.text == "⚙Показать/Поменять информацию о себе⚙":
        arg_data = DB_worker.get_data(DB_worker.name_bd, message.from_user.id)[0]
        print(arg_data)
        await bot.send_message(message.from_user.id, f"Ваш город : {arg_data[1]}\nВаша занятость: {arg_data[2]}",
                               reply_markup=menu.changeInfo)

    elif message.text == "Мой город":
        await ChangeCity.city.set()
        await bot.send_message(message.from_user.id,
                               "Введите название вашего города на русском или украинском\n"
                               "(Введите \"Украина\", если хотите искать работу по всей стране)",
                               reply_markup=closeMenu)

    elif message.text == "Вид занятости":
        await ChangeEmp.emp.set()
        await bot.send_message(message.from_user.id, "Выберете тип занятости",
                               reply_markup=menu.EmpType)


    elif message.text == "Меню":
        await bot.send_message(message.from_user.id, "Возвращаемся в меню",
                               reply_markup=menu.mainMenu)


@dp.message_handler(state=ChangeCity.city)
async def bot_city(message: types.Message, state: FSMContext):
    DB_worker.update_city_name(DB_worker.name_bd, message.from_user.id, message.text.lower().title())
    print(DB_worker.get_data(DB_worker.name_bd))
    await state.finish()
    await bot.send_message(message.from_user.id,
                           "Данные успешно сохранены",
                           reply_markup=menu.changeInfo)


@dp.message_handler(state=ChangeEmp.emp)
async def bot_emp(message: types.Message, state: FSMContext):
    arg_answer = "Некорректный ввод (данные не сохранены)"
    if message.text in ["Полная занятость", "Неполная занятость", "Удаленная работа", "Любой график работы"]:
        DB_worker.update_busyness(DB_worker.name_bd, message.from_user.id, message.text)
        arg_answer = "Данные успешно сохранены"

    print(DB_worker.get_data(DB_worker.name_bd))
    print(message.text)
    await bot.send_message(message.from_user.id, arg_answer, reply_markup=menu.changeInfo)
    await state.finish()


@dp.message_handler(state=SearchVacs.srch)
async def bot_search(message: types.Message, state: FSMContext):
    global main_all_vac
    global main_search_words
    global counter
    counter = 0
    main_all_vac = []
    all_rabota_ua_vacs = []
    all_work_ua_ua_vacs = []
    arg_data = DB_worker.get_data(DB_worker.name_bd, main_user_id)
    temp_arg_city_name = ""
    temp_arg_busyness = ""
    if len(arg_data) and arg_data[0][1] is not None and arg_data[0][2] is not None:
        temp_arg_city_name = arg_data[0][1]
        temp_arg_busyness = arg_data[0][2]
    main_search_words = message.text
    print(main_search_words.strip(),
          temp_arg_city_name,
          temp_arg_busyness)
    await bot.send_message(message.from_user.id, "Подождите немного...", reply_markup=menu.Search)
    await async_rabota_ua.gather_all_vacancies(all_rabota_ua_vacs, main_search_words.strip(),
                                               temp_arg_city_name,
                                               temp_arg_busyness)
    await async_work_ua.gather_all_vacancies(all_work_ua_ua_vacs, main_search_words.strip(), temp_arg_city_name,
                                             temp_arg_busyness)
    main_all_vac.append(all_rabota_ua_vacs)
    main_all_vac.append(all_work_ua_ua_vacs)
    await state.finish()

    print(main_all_vac)
    print(len(main_all_vac[0]), len(main_all_vac[1]))
    await bot.send_message(message.from_user.id, "Сайт rabota.ua", reply_markup=menu.Search)
    if (counter + 1) * 5 < len(main_all_vac[0]):
        for temp in main_all_vac[0][counter * 5:(counter + 1) * 5]:
            await bot.send_message(message.from_user.id, temp, reply_markup=menu.Search)
    elif (counter + 1) * 5 > len(main_all_vac[0]) > counter * 5:
        for temp in main_all_vac[0][counter * 5:]:
            await bot.send_message(message.from_user.id, temp, reply_markup=menu.Search)
    else:
        await bot.send_message(message.from_user.id, "Вакансий больше нет (rabota.ua)", reply_markup=menu.Search)

    await bot.send_message(message.from_user.id, "Сайт work.ua", reply_markup=menu.Search)
    if (counter + 1) * 5 < len(main_all_vac[1]):
        for temp in main_all_vac[1][counter * 5:(counter + 1) * 5]:
            await bot.send_message(message.from_user.id, temp, reply_markup=menu.Search)
    elif (counter + 1) * 5 > len(main_all_vac[1]) > counter * 5:
        for temp in main_all_vac[1][counter * 5:]:
            await bot.send_message(message.from_user.id, temp, reply_markup=menu.Search)
    else:
        await bot.send_message(message.from_user.id, "Вакансий больше нет (work.ua)", reply_markup=menu.Search)
    counter += 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
