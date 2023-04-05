from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types, exceptions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import logging, db, asyncio, random, datetime
from glQiwiApi import QiwiWallet, QiwiWrapper



bot = Bot(token="") #токин
admin = #chat id
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

btn1 = KeyboardButton('📛 个人资料')
btn2 = KeyboardButton('🎲 骰子')
btn3 = KeyboardButton('🎰 轮盘赌')
btn4 = KeyboardButton('🏀 篮球')
btn5 = KeyboardButton('⚽ 足球')
btn6 = KeyboardButton('🎯 飞镖')
btn7 = KeyboardButton('👑 玩家排行榜')
btn8 = KeyboardButton('🎖 购买积分')
btn9 = KeyboardButton('⚡ 群聊排行榜')



basic = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1).add(btn2, btn3, btn4).add(btn5, btn6).add(btn7, btn8, btn9)

class Send(StatesGroup):
	msg = State()

@dp.message_handler(commands=['send'])
async def send(msg: types.Message):

	if msg.chat.id == 1020329422:
		await Send.msg.set()
		await msg.reply('Введите сообщение \n /close для отмены')
	else:
		pass


@dp.message_handler(state=Send.msg, content_types=['text', 'photo'])
async def send_messag(message: types.Message, state: FSMContext):

	ides = db.all()

	y = 0
	n = 0

	if message.content_type == 'text':
		if message.text == '/close':
			pass
		else:

			for i in ides:
				try:
					await bot.send_message(i[0], message.text)
					y += 1
				except Exception as e:
					n += 1
					print(e)
			await message.reply(f'Отправлено \n{y} - отправлено\n{n} - Не отправлено')
	else:
		if message.text == '/close':
			pass
		else:
			for i in ides:
				try:
					await bot.send_photo(i[0], photo=message.photo[0].file_id,caption=message.caption)
					y += 1
				except:
					n += 1
			await message.reply(f'Отправлено \n{y} - отправлено\n{n} - Не отправлено')

	await state.finish()


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
	if db.check(msg) is None:
		db.main(msg)
	else:
		pass
	await msg.reply('''
Добро пожаловать👋
''', reply_markup = basic)


@dp.message_handler(content_types=['dice'])
async def diceall(msg: types.Message):
	if msg.dice.emoji == '🎲':
		await msg.reply('Подтвердите игру', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Подтвердить✅', callback_data='cube')))
	if msg.dice.emoji == '🎰':
		await msg.reply('Подтвердите игру', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Подтвердить✅', callback_data='casino')))
	if msg.dice.emoji == '🏀':
		await msg.reply('Подтвердите игру', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Подтвердить✅', callback_data='basket')))
	if msg.dice.emoji == '🎯':
		await msg.reply('Подтвердите игру', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Подтвердить✅', callback_data='darts')))

	print(msg)

@dp.message_handler()
async def all(msg: types.Message):
	if msg.text == '📛 Профиль':
		await profile(msg)
	if msg.text == '🎲 Кости':
		await msg.reply('Подтвердите игру', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Подтвердить✅', callback_data='cube')))
	if msg.text == '🎰 Рулетка':
		await msg.reply('Подтвердите игру', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Подтвердить✅', callback_data='casino')))
	if msg.text == '🏀 Баскет':
		await msg.reply('Подтвердите игру', reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Подтвердить✅', callback_data='basket')))
	if msg.text == '👑 Топ игроков':
		info = db.all()

		btn1 = InlineKeyboardButton(f'👑 {info[0][3]} 🎖{info[0][1]}', callback_data='123049')
		btn2 = InlineKeyboardButton(f'⭐ {info[1][3]} 🎖{info[1][1]}', callback_data='123049')
		btn3 = InlineKeyboardButton(f'🎀 {info[2][3]} 🎖{info[2][1]}', callback_data='123049')
		markup = InlineKeyboardMarkup().add(btn1).add(btn2).add(btn3)

		await msg.reply('👑Топ 3 игрока👑', reply_markup = markup)
	if msg.text == '🎖 Купить очки':
		btn1 = InlineKeyboardButton('100🎖 9Р ХИТ', callback_data='100r')
		btn2 = InlineKeyboardButton('1000🎖 99Р Выгодно', callback_data='1000r')
		btn3 = InlineKeyboardButton('10000🎖 599Р Скидка', callback_data='10000r')

		markup = InlineKeyboardMarkup().add(btn1).add(btn2, btn3)

		await msg.reply('Выберите сколько репутации хотите купить', reply_markup=markup)
	if msg.text == '⚡ Топ бесед':
		info = db.allbesed()

		btn1 = InlineKeyboardButton(f'👑 {info[0][3]} 🎖{info[0][1]}', callback_data='123049')
		btn2 = InlineKeyboardButton(f'⭐ {info[1][3]} 🎖{info[1][1]}', callback_data='123049')
		btn3 = InlineKeyboardButton(f'🎀 {info[2][3]} 🎖{info[2][1]}', callback_data='123049')
		markup = InlineKeyboardMarkup().add(btn1).add(btn2).add(btn3)

		await msg.reply('👑Топ 3 беседы', reply_markup=markup)

@dp.callback_query_handler(text="100r")
async def r100(call: types.CallbackQuery, state: FSMContext):
	msg = call.message
	await msg.delete()

	await buyrub(msg, 9,100)

@dp.callback_query_handler(text="1000r")
async def r1000(call: types.CallbackQuery, state: FSMContext):
	msg = call.message
	await msg.delete()

	await buyrub(msg, 99, 1000)

@dp.callback_query_handler(text="10000r")
async def r10000(call: types.CallbackQuery, state: FSMContext):
	msg = call.message
	await msg.delete()

	await buyrub(msg, 599, 10000)



@dp.callback_query_handler(text="casino")
async def casino(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()

	await rulet(call.message)

@dp.callback_query_handler(text="cube")
async def cube(call: types.CallbackQuery, state: FSMContext):
	msg = call.message
	await msg.delete()

	await cubikdone(msg)

@dp.callback_query_handler(text="rulet")
async def rulet(call: types.CallbackQuery, state: FSMContext):
	msg = call.message
	await msg.delete()

	await cubikdone(msg)

@dp.callback_query_handler(text="basket")
async def basket(call: types.CallbackQuery, state: FSMContext):
	msg = call.message
	await msg.delete()

	await basketboll(msg)

@dp.callback_query_handler(text="football")
async def football(call: types.CallbackQuery, state: FSMContext):
	msg = call.message
	await msg.delete()

	await football(msg)

@dp.callback_query_handler(text="darts")
async def darts(call: types.CallbackQuery, state: FSMContext):
	msg = call.message
	await msg.delete()

	await darts(msg)


async def profile(msg):
	info = db.check(msg)
	name = msg.chat.username
	if name == None:
		name = msg.chat.title

	markup = InlineKeyboardMarkup()
	markup.add(InlineKeyboardButton(f'📛:{name}', callback_data = '213')).add(InlineKeyboardButton(f'⭐: {info[1]}', callback_data = '213')).add(InlineKeyboardButton(f'👀Игр сыграно: {info[2]}', callback_data = '213'))

	await msg.answer(f'''
🎩Ваш профиль🎩
''', reply_markup = markup)

async def basketboll(msg):
	info = db.check(msg)

	dice = await msg.answer_dice(emoji="🏀")
	dice_value = dice.dice.value

	await asyncio.sleep(5)

	if dice_value in [1, 2, 3]:
		if info[1] == 0:
			await msg.answer(f'❌Вы проиграли -0🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='basket')))
		else:
			await msg.answer(f'❌Вы проиграли -6🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='basket')))
			db.minusrep(msg, 6)
	else:
		await msg.answer(f'✅Вы выйграли +6🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='basket')))
		db.addrep(msg, 6)
	db.addgame(msg)

async def football(msg):
	info = db.check(msg)

	dice = await msg.answer_dice(emoji="⚽")
	dice_value = dice.dice.value

	await asyncio.sleep(5)

	if dice_value in [1, 2, 3]:
		if info[1] == 0:
			await msg.answer(f'❌Вы проиграли -0🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='football')))
		else:
			await msg.answer(f'❌Вы проиграли -6🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='football')))
			db.minusrep(msg, 6)
	else:
		await msg.answer(f'✅Вы выйграли +6🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='football')))
		db.addrep(msg, 6)
	db.addgame(msg)

async def rulet(msg):
	info = db.check(msg)

	dice = await msg.answer_dice(emoji="🎰")
	dice_value = dice.dice.value

	await asyncio.sleep(2)

	if dice_value in (1, 22, 43):
		await msg.answer(f'Вы выйграли +18🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='casino')))
		db.addrep(msg, 18)
	elif dice_value in (16, 32, 48):
		await msg.answer(f'Вы выйграли +6🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='casino')))
		db.addrep(msg, 6)
	elif dice_value == 64:
		await msg.answer(f'JACKPOT!! +50🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='casino')))
		db.addrep(msg, 50)
	else:
		if info[1] == 0:
			await msg.answer(f'Вы проиграли -0🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='casino')))
		else:
			await msg.answer(f'Вы проиграли -6🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='casino')))
			db.minusrep(msg, 6)


async def darts(msg):
	info = db.check(msg)

	dice = await msg.answer_dice(emoji="🎯")
	dice_value = dice.dice.value

	await asyncio.sleep(3)

	if dice_value in [1, 2, 3]:
		if info[1] == 0:
			await msg.answer('❌Вы проиграли -0🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='darts')))
		else:
			await msg.answer('❌Вы проиграли -6🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='darts')))
			db.minusrep(msg, 6)
	if dice_value in [4, 5]:
		await msg.answer('✅Вы выйграли +6🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='darts')))
		db.addrep(msg, 6)
	if dice_value == 6:
		await msg.answer('⭐ВЫ ВЫЙГРАЛИ +12🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='darts')))
		db.addrep(msg, 12)

	db.addgame(msg)

async def cubikdone(msg):
	info = db.check(msg)

	bot_dice = await bot.send_dice(msg.chat.id, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Противник❌', callback_data='23214')))
	user_dice = await bot.send_dice(msg.chat.id, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('ВЫ✅', callback_data='23214')))

	bot_dice = bot_dice.dice.value
	user_dice = user_dice.dice.value

	await asyncio.sleep(4)

	if bot_dice == user_dice:
		await msg.answer('⚠Ничья')
	if bot_dice > user_dice:
		if info[1] == 0:
			await msg.answer(f'❌Вы проиграли -0🎖\n\nПротивник +6🎖\nВы -0🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='cube')))
		else:	
			await msg.answer(f'❌Вы проиграли -6🎖\n\nПротивник +6🎖\nВы -6🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='cube')))
			db.minusrep(msg, 6)
	if bot_dice < user_dice:
		await msg.answer(f'✅Вы выиграли +6🎖\n\nПротивник -6🎖\nВы +6🎖', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Еще раз⏭', callback_data='cube')))
		db.addrep(msg, 6)

	db.addgame(msg)

async def buyrub(msg, cena, rep):
	qiwi = ''#сюда токен p2p qiwi
	async with QiwiWrapper(secret_p2p=qiwi) as w:
		code = random.randint(100, 999)
		bill = await w.create_p2p_bill(
			amount=cena,
			comment=
			f'Покупка рублей на сумму {cena}Р, Вы получите {rep}🎖\nCode - {code}',
			life_time=datetime.datetime.now() + datetime.timedelta(minutes=10))

		btn1 = types.InlineKeyboardButton(f'Оплатить {cena}Р', url=bill.pay_url)
		markup = types.InlineKeyboardMarkup().add(btn1)

		a = await msg.answer(f'У вас есть 10 минут для оплаты счет', reply_markup=markup)
		seconds = 600
		repeats = [1 for i in range(0, seconds)]
		for i in repeats:
			check = await w.check_p2p_bill_status(bill_id=bill.id)
			await asyncio.sleep(5)
			if check == "PAID":

				await bot.send_message(admin, f'Topped up balance {cena}\nCode-{code}')
				await msg.answer(f'Вы успешно купили {rubs} рублей')

				db.addrep(msg.chat.id, rep)

				break
			if check == 'EXPIRED':
				await a.edit_text("Вы не успели((")
				break

			await asyncio.sleep(10)


if __name__ == '__main__':

	executor.start_polling(dp, skip_updates=True)