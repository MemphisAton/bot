import random

from tkn import tkn

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

BOT_TOKEN: str = tkn
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

ATTEMPTS: int = 5
users: dict = {}


# возврат случайного числа
def get_random_number() -> int:
    random_number = random.randint(1, 100)
    return random_number


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('''Привет!
    Давайте сыграем в игру "Угадай число"?
    Чтобы получить правила игры и список доступных
    команд - отправьте команду /help''')
    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f'''Правила игры:
                        Я загадываю число от 1 до 100,
                        а вам нужно его угадать
                        У вас есть {ATTEMPTS} попыток
                        Доступные команды:
                        /help - правила игры и список команд
                        /cancel - выйти из игры
                        /stat - посмотреть статистику
                        Давай сыграем?''')


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'''Всего игр сыграно:
                        {users[message.from_user.id]["total_games"]}
                        Игр выиграно: 
                        {users[message.from_user.id]["wins"]}''')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('''Вы вышли из игры. Если захотите сыграть
                             снова - напишите об этом''')
        users[message.from_user.id]['in_game'] = False
    await message.answer('''А мы итак с вами не играем.
                        Может, сыграем разок?''')


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'y']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('''Ура!Я загадал число от 1 до 100,
                             попробуй угадать!''')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer('''Пока мы играем в игру я могу
                             реагировать только на числа от 1 до 100
                             и команды /cancel и /stat''')


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'n']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('''Жаль :( Если захотите поиграть - просто
                             напишите об этом''')
    else:
        await message.answer('''Мы же сейчас с вами играем. Присылайте,
                             пожалуйста, числа от 1 до 100''')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('''Ура!!! Вы угадали число!
                                 Может, сыграем еще?''')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Мое число меньше')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Мое число больше')
            users[message.from_user.id]['attempts'] -= 1

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(f'''К сожалению, у вас больше не осталось
                                попыток. Вы проиграли :( Мое число 
                                было {users[message.from_user.id]["secret_number"]}
                                Давайте сыграем еще?''')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('''Мы же сейчас с вами играем.
                             Присылайте, пожалуйста, числа от 1 до 100''')
    else:
        await message.answer('''Я довольно ограниченный бот, давайте
                             просто сыграем в игру.''')


if __name__ == '__main__':
    dp.run_polling(bot)
