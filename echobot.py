from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from tkn import tkn

API_TOKEN: str = tkn

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()




# отработает на отправку /start
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nЯ создан, что бы заебать тебя')


## отработает на отправку /help
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и ты увидишь магию')


# отработает на отправку любого сообщения
@dp.message()
async def send_echo(message: Message):
    # из за этой части отлавливает стикеры, но выскакивают ошибки не влияющие на работу бота
    # if message.sticker:
    #     await message.answer_sticker(message.sticker.file_id)
    if message.text and 'отключу' in message.text.lower():
        await message.answer(
            f'попробуй блять, {message.from_user.first_name} я знаю больше чем ты думаешь, кажанный мешок')
    else:
        try:
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            await message.reply(text='Данный тип апдейтов не поддерживается '
                                     'методом send_copy')


# обязательно регистрируем фуркции(хендлеры), я же это сделал спомощью декораторов,
# но можно и так:
# dp.message.register(process_help_command, Command(commands=['start']))
# dp.message.register(process_start_command, Command(commands=['help']))
# dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)
