from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMenu = KeyboardButton("Меню")

btnSrch = KeyboardButton("🔎Поиск работы🔎")
btnHelp = KeyboardButton("📃Помощь📃")
btnChangeInfo = KeyboardButton("⚙Показать/Поменять информацию о себе⚙")
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(btnSrch).add(btnHelp).add(btnChangeInfo)

#ChangeInfo
btnCity = KeyboardButton("Мой город")
btnEmp = KeyboardButton("Вид занятости")
changeInfo = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(btnCity, btnEmp).add(btnMenu)

#EmpType
btnE1 = KeyboardButton("Полная занятость")
btnE2 = KeyboardButton("Неполная занятость")
btnE3 = KeyboardButton("Удаленная работа")
btnE4 = KeyboardButton("Любой график работы")
EmpType = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(btnE1, btnE2).add(btnE3, btnE4)

#Search
btnS10 = KeyboardButton("💬Показать еще 10💬")
Search = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(btnS10).add(btnMenu)