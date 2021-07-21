import telebot
from telebot import types
import datetime
import pymysql

bot = telebot.TeleBot('1411767260:AAHYvwP6Iv4bJcbwfCTRnpTTiEsKh_PHo3I')

helps = False
ids = ''
dep = False
keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
dateday = [0,0,0]
info = ''
summ = False
send_money = False
day = 0

@bot.message_handler(commands = ['start'])
def get_text_messages(message):
	global keyboard
	db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
	cursor = db.cursor()
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button_deposit = types.KeyboardButton(text="Мой депозит💵")
	button_partner = types.KeyboardButton(text="Мои партнери🤝")
	button_send = types.KeyboardButton(text="Задать вопрос❓")
	button_settings = types.KeyboardButton(text="Настройка⚙️")
	keyboard.add(button_deposit, button_partner, button_send, button_settings)
	bot.send_message(message.from_user.id, f"Привет {message.from_user.first_name}", reply_markup=keyboard)
	cursor.execute("""SELECT id FROM users""")
	rows = cursor.fetchall()
	register = False
	if len(rows) == 0:
		cursor.execute("""INSERT INTO users (id, name, account, partner, invested) VALUES (%s, %s, %s, %s, %s)""", (int(message.from_user.id), message.from_user.first_name, int(0), message.text.replace("/start", ""), int(0)))
	else:
		for row in rows:
			print(row)
			if row[0] == int(message.from_user.id):
				register = True
				break
		if register == False:
			cursor.execute("""INSERT INTO users (id, name, account, partner, invested) VALUES (%s, %s, %s, %s, %s)""", (int(message.from_user.id), message.from_user.first_name, int(0), message.text.replace("/start", ""), int(0)))
	db.commit()
	db.close()

@bot.message_handler(commands = ['help'])
def help(message):
	global keyboard
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button1 = types.KeyboardButton(text="Назад")
	keyboard.add(button1)
	bot.send_message(message.from_user.id, "Напиши вопрос!", reply_markup=keyboard)
	global helps
	helps = True

@bot.message_handler(commands = ['deposit'])
def deposit(message):
	global keyboard
	global account
	global invested
	db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
	cursor = db.cursor()
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button1 = types.KeyboardButton(text="Пополнить")
	button2 = types.KeyboardButton(text="Вивести")
	button3 = types.KeyboardButton(text="Открить депозит")
	button4 = types.KeyboardButton(text="Мои активи")
	button5 = types.KeyboardButton(text="Назад")
	keyboard.add(button1, button2, button3, button4, button5)
	cursor.execute("""SELECT * FROM users""")
	cursor.execute("""SELECT * FROM users WHERE id = %s""", (message.from_user.id))
	info = cursor.fetchall()
	bot.send_message(message.from_user.id, f"Ваш баланс: {info[0][2]}$ \nВсего инвестировано: {info[0][4]}$", reply_markup=keyboard)
	db.close()

@bot.message_handler(commands=['opend'])
def openn(message):
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	button = telebot.types.InlineKeyboardButton(text='8%-30 дней', callback_data='8% на 30 дней')
	button1 = telebot.types.InlineKeyboardButton(text='18%-60 дней', callback_data='18% на 60 дней')
	button2 = telebot.types.InlineKeyboardButton(text='28%-90 дней', callback_data='28% на 90 дней')
	markup.add(button, button1, button2)
	bot.send_message(chat_id=message.chat.id, text='Вибирете процентную ставку и срок депозита',  reply_markup=markup)

@bot.message_handler(commands=['actives'])
def activess(message):
	global keyboard
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button_deposit = types.KeyboardButton(text="Мой депозит💵")
	button_partner = types.KeyboardButton(text="Мои партнери🤝")
	button_send = types.KeyboardButton(text="Задать вопрос❓")
	button_settings = types.KeyboardButton(text="Настройка⚙️")
	keyboard.add(button_deposit, button_partner, button_send, button_settings)
	db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM actives WHERE id = %s""", (message.from_user.id))
	actives = cursor.fetchall()
	if len(actives) != 0:
		i = 1
		for active in actives:
			bot.send_message(message.from_user.id, f'''Актив №{i}:
					Сума: {active[1]}$
					Срок: {active[2]} дней
					Доходность: {active[3]}%
					Итоговая прибль: {active[4]}$
					Дата получения дохода: {active[5]}

					''', reply_markup = keyboard)
			i += 1
	else:
		bot.send_message(message.from_user.id, 'У вас нет откритих активов!', reply_markup = keyboard)
	db.close()

@bot.message_handler(commands = ['admin'])
def admin(message):
	if message.from_user.id == 721921999:
		db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM users""")
		markup = telebot.types.InlineKeyboardMarkup(row_width=1)
		button = telebot.types.InlineKeyboardButton(text='Рассилка', callback_data='send')
		button1 = telebot.types.InlineKeyboardButton(text='Зачислить', callback_data='send_money')
		button2 = telebot.types.InlineKeyboardButton(text='Откритие депозити', callback_data='open_deposites')
		markup.add(button, button1, button2)
		bot.send_message(message.chat.id, f'Админ меню: \nПользователей в боте: {len(cursor.fetchall())}',  reply_markup=markup)
		db.close()

@bot.message_handler(commands=['partners'])
def partners(message):
	db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM users WHERE partner = %s""", (message.from_user.id))
	partners = cursor.fetchall()
	bot.send_message(message.from_user.id, f'Партнерская програма: \n \n Ваши приглашения: \n {len(partners)} уровень - {len(partners)} партнеров - 0$ заработано \n \n Ваша партнерская ссилка: \n https://t.me/helpppinvestttbot?start={message.from_user.id} \n \n Приглашайте партнеров и получайте: \n 10% от первого пополнения.')
	db.close()

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	global dep
	global info
	global date
	global keyboard
	global account
	global invested
	global price
	global idss
	global admin
	global send_money
	if call.data == '8% на 30 дней' or call.data == '18% на 60 дней' or call.data == '28% на 90 дней':
		info = call.data.replace("на", "")
		info = info.replace("дней", "") 
		bot.send_message(call.message.chat.id, f"""Инвестиция под {call.data}
			Введите суму инвестиции от 50$""")
		dep = True
	if call.data == 'Ok' and dep == True:
		db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
		cursor = db.cursor()
		if len(info) == 7:
			cursor.execute("""INSERT INTO `actives` (`id`, `sum`, `timess`, `interest`, `profit`, `dates`) VALUES (%s, %s, %s, %s, %s, %s)""", (str(idss), str(price), str(int(info[4]+info[5])), str(int(info[0])), str(int(int(price) * int(info[0]) / 100)), date))
		if len(info) == 8:
			cursor.execute("""INSERT INTO `actives` (`id`, `sum`, `timess`, `interest`, `profit`, `dates`) VALUES (%s, %s, %s, %s, %s, %s)""", (str(idss), str(price), str(int(info[5]+info[6])), str(int(info[0]+info[1])), str(int(int(price) * int(info[0]+info[1]) / 100)), date))
		cursor.execute("""UPDATE users SET account = account - %s, invested = invested + %s WHERE id = %s""", (price, price, call.message.chat.id))
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		button_deposit = types.KeyboardButton(text="Мой депозит💵")
		button_partner = types.KeyboardButton(text="Мои партнери🤝")
		button_send = types.KeyboardButton(text="Задать вопрос❓")
		button_settings = types.KeyboardButton(text="Настройка⚙️")
		keyboard.add(button_deposit, button_partner, button_send, button_settings)
		bot.send_message(call.message.chat.id, '''Депозит успешно открит
			(Активние депозити можете посмотреть в разделе "Мои активи")''', reply_markup=keyboard)
		dep = False
		db.commit()
		db.close()
	if call.data == 'Back' and dep == True:
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		button_deposit = types.KeyboardButton(text="Мой депозит💵")
		button_partner = types.KeyboardButton(text="Мои партнери🤝")
		button_send = types.KeyboardButton(text="Задать вопрос❓")
		button_settings = types.KeyboardButton(text="Настройка⚙️")
		keyboard.add(button_deposit, button_partner, button_send, button_settings)
		bot.send_message(call.message.chat.id,'Главное меню', reply_markup=keyboard)
		dep = False
	if call.data == 'send':
		bot.send_message(call.message.chat.id, 'Напишите сообщения на отправку!')
		admin = True
	if call.data == 'open_deposites':
		db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM actives""")
		actives = cursor.fetchall()
		if len(actives) != 0:
			i = 1
			for active in actives:
				bot.send_message(call.message.chat.id, f'''Актив №{i}:
						Id: {active[0]}
						Сума: {active[1]}$
						Срок: {active[2]} дней
						Доходность: {active[3]}%
						Итоговая прибль: {active[4]}$
						Дата получения дохода: {active[5]}

						''', reply_markup = keyboard)
				i += 1
		else:
			bot.send_message(call.message.chat.id, 'Нету откритих активов!')
		db.close()
	if call.data == 'send_money':
		bot.send_message(call.message.chat.id, 'Введите id пользователя')
		send_money = True

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global helps
	global ids
	global keyboard
	global dep
	global info
	global date
	global idss
	global admin
	global send_money
	global summ
	global price
	global idsss
	global day
	if day != datetime.date.today():
		db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
		cursor = db.cursor()
		cursor.execute("""SELECT dates, id, profit FROM actives""")
		dates = cursor.fetchall()
		for date in dates:
			if date[0] <= datetime.date.today():
				cursor.execute("""UPDATE users SET account = account + %s WHERE id = %s""", (date[2], date[1]))
				cursor.execute("""DELETE FROM actives WHERE id = %s""", (date[1]))
		db.commit()
		db.close()
		day = datetime.date.today()
	if message.text == "Назад":
		helps = False
		dep = False
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		button_deposit = types.KeyboardButton(text="Мой депозит💵")
		button_partner = types.KeyboardButton(text="Мои партнери🤝")
		button_send = types.KeyboardButton(text="Задать вопрос❓")
		button_settings = types.KeyboardButton(text="Настройка⚙️")
		keyboard.add(button_deposit, button_partner, button_send, button_settings)
		bot.send_message(message.from_user.id,'Главное меню', reply_markup=keyboard)
	if helps == True:
		bot.send_message('721921999', f"""Вопрос от {message.from_user.first_name}; id: {message.from_user.id}:
		{message.text}""")
		ids = message.from_user.id
		helps = False
	if message.from_user.id == 721921999 and ids != '':
		bot.send_message(ids, f"""Ответ:
		{message.text}""")
		ids = ''
		bot.send_message(message.from_user.id, "Отправлено")
	if message.text == 'Задать вопрос❓':
		help(message)

	if message.text == 'Мой депозит💵':
		deposit(message)

	if message.text == 'Открить депозит':
		openn(message)

	if dep == True:
		try: 
			int(message.text)
			db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
			cursor = db.cursor()
			cursor.execute("""SELECT * FROM users WHERE id = %s""", (message.from_user.id))
			user = cursor.fetchall()
			markup = telebot.types.InlineKeyboardMarkup(row_width=1)
			button = telebot.types.InlineKeyboardButton(text='Подтвердить', callback_data='Ok')
			button1 = telebot.types.InlineKeyboardButton(text='Назад', callback_data='Back')
			markup.add(button, button1)
			if int(message.text) < 50:
				bot.reply_to(message, 'Введите суму више 50$!')
			if int(user[0][2]) < 50:
				bot.reply_to(message, 'На вашем счету менше 50$. Пополните пожалуста счет!')
				dep = False
			elif int(message.text) > int(user[0][2]):
				bot.reply_to(message, 'Простите но на вашем счету нету столько денег.')
			if int(message.text) >= 50 and int(message.text) <= int(user[0][2]):
				price = message.text
				if len(info) == 7:
					date = datetime.date.today() + datetime.timedelta(days=int(info[4]+info[5]))
					bot.reply_to(message, f'''Подробности и подтверждение:
					Сума: {price}$
					Срок: {info[4]+info[5]} дней
					Доходность: {info[0]}%
					Итоговая прибль: {str(int(int(price) * int(info[0]) / 100))}$
					Дата получения дохода: {date.day}.{date.month}.{date.year}''', reply_markup = markup)
				if len(info) == 8:
					date = datetime.date.today() + datetime.timedelta(days=int(info[5]+info[6]))
					bot.reply_to(message, f'''Подробности и подтверждение:
					Сума: {price}$
					Срок: {info[5]+info[6]} дней
					Доходность: {info[0]+info[1]}%
					Итоговая прибль: {str(int(int(price) * int(info[0]+info[1]) / 100))}$
					Дата получения дохода: {date.day}.{date.month}.{date.year}''', reply_markup = markup)
				idss = message.from_user.id
			db.close()
		except:
			bot.reply_to(message, 'Введите пожалуста целое число!')

	if message.text == 'Мои активи':
		activess(message)

	if message.text == 'Мои партнери🤝':
		partners(message)

	if admin == True:
		db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM users""")
		users = cursor.fetchall()
		for user in users:
			if user[0] == 721921999:
				pass
			else:
				bot.send_message(user[0], message.text)
		db.close()
		bot.send_message(message.from_user.id, 'Сообщения успешно розислано!')
		admin = False

	if summ == True and idsss != '':
		try:
			int(message.text)
			db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='users', charset='utf8mb4')
			cursor = db.cursor()
			cursor.execute("""UPDATE users SET account = account + %s WHERE id = %s""", (message.text, idsss))
			db.commit()
			db.close()
			summ = False
			bot.send_message(message.from_user.id, "Перечислено!")
		except: 
			bot.send_message(message.from_user.id, "Введите целое число")

	if send_money == True:
		bot.reply_to(message, 'Введите суму для пополнения')
		summ = True
		send_money = False
		idsss = message.text

bot.polling(none_stop=True, interval=0)