import datetime
import os
import redis
from dotenv import load_dotenv
from translator import message_cetus
from statusCetus import check_five_min
from vkbottle.bot import Bot, Message
from get_arbitration import get_data_about_arbitration


load_dotenv()
API_token = os.getenv('API_KEY_SPARLEX')


chat_db = redis.Redis(host='localhost', port=6379, db=2)

bot = Bot(token=API_token)
bot.labeler.vbml_ignore_case = True


@bot.on.message(text="инфо")
async def info(message: Message):
    await message.answer( 'Привет, я бот, которого сделал жукич.'
                                                        '\nКак мной пользоваться: '
                                                        '\n1) напишите "рассылка" чтобы настроить самостоятельные уведомления '
                                                        '\n2) напишите "цетус" чтобы узнать время суток на Цетус'
                                                        '\n3) напишите "арбитраж" чтобы узнать информацию об арбитраже'
                                                        '\n4) напишите "ночной режим" чтобы выключить самостоятельные уведомления'
                                                        '\n5) напишите "статус" чтобы проверить режим самостоятельных уведомлений'
    )


@bot.on.message(text="цетус")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    print(chat_db.keys())
    await message.answer(message_cetus())


@bot.on.message(text="рассылка")
async def add_to_list_of_chats_in_notify(message: Message):

    group_info = message.peer_id

    if chat_db.get(group_info) == bytes('off', 'utf-8'):
        chat_db.set(group_info, 'on')
        await message.answer("Режим рассылки включен")

    elif chat_db.get(group_info) == bytes('on', 'utf-8'):
        await message.answer("Режим рассылки у вас уже включен")

    elif not(chat_db.get(group_info)):
        chat_db.set(group_info, 'on')
        await message.answer("Режим рассылки включен")


@bot.on.message(text="ночной режим")
async def add_to_list_of_chats_in_slee(message: Message):

    group_info = message.peer_id

    if chat_db.get(group_info) == bytes('on', 'utf-8'):
        chat_db.set(group_info, 'off')
        await message.answer("Ночной режим включен")

    elif chat_db.get(group_info) == bytes('off', 'utf-8'):
        await message.answer("Ночной режим у вас уже включен")

    elif not(chat_db.get(group_info)):
        chat_db.set(group_info, 'off')
        await message.answer("Ночной режим включен")


@bot.on.message(text='статус')
async def check_status(message: Message):

    group_info = message.peer_id

    if chat_db.get(group_info) == bytes('on', 'utf-8'):
        await message.answer("Режим рассылки включен")
    else:
        await message.answer("Режим рассылки выключен")


@bot.on.message(text='арбитраж')
async def arbitrage_chek(message: Message):
    data_arbitration = get_data_about_arbitration()

    await message.answer(
                        f"Место: {data_arbitration['node']}"
                        f"\nРежим: {data_arbitration['type']}"
                        f"\nВраги: {data_arbitration['enemy']}"
                        f"\nОсталось: {data_arbitration['left_time']} мин"
    )


@bot.loop_wrapper.interval(seconds=200)
async def notifications():

    if check_five_min() == 'night':

        keys = chat_db.keys()

        for k in keys:
            if chat_db.get(k) == bytes('on', 'utf-8'):
                await bot.api.messages.send(peer_id=k.decode('utf-8'), message="ВСЕМ ЕБАТЬ ГЕЙДАЛОНОВ", random_id=0)

    elif check_five_min() == 'day':

        keys = chat_db.keys()

        for k in keys:
            if chat_db.get(k) == bytes('on', 'utf-8'):
                await bot.api.messages.send(peer_id=k.decode('utf-8'), message="Ночь скоро закончится", random_id=0)


@bot.loop_wrapper.interval(hours=1)
async def status_notification():
    current_hour = datetime.datetime.now()
    if current_hour.hour == 8:

        keys = chat_db.keys()

        for k in keys:
            if chat_db.get(k) == bytes('off', 'utf-8'):
                await bot.api.messages.send(peer_id=k.decode('utf-8'), message="Не хотите ли включить рассылку?", random_id=0)

    elif current_hour.hour == 23:

        keys = chat_db.keys()

        for k in keys:
            if chat_db.get(k) == bytes('on', 'utf-8'):
                await bot.api.messages.send(peer_id=k.decode('utf-8'), message="Не хотите ли выключить рассылку?", random_id=0)


bot.run_forever()