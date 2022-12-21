import datetime, os
from dotenv import load_dotenv
from translator import message_cetus
from statusCetus import check_five_min
from vkbottle.bot import Bot, Message
from get_data_from_WFHub import get_date_from_wfhub


load_dotenv()
API_token = os.getenv('API_KEY_SPARLEX')


list_of_chats_in_notify = []
list_of_chats_in_sleep = []

bot = Bot(token=API_token)
bot.labeler.vbml_ignore_case = True


@bot.loop_wrapper.interval(seconds=60)
async def redis_cache():
    await get_date_from_wfhub()


@bot.on.message(text="инфо")
async def info(message: Message):
    await message.answer( 'Привет, я бот, которого сделал жукич.'
                                                        '\nКак мной пользоваться: '
                                                        '\n1) напишите "рассылка" чтобы настроить самостоятельные уведомления '
                                                        '\n2) напишите "цетус" чтобы узнать время суток на Цетус'
                                                        '\n3) напишите "ночной режим" чтобы выключить самостоятельные уведомления'
                                                        '\n4) напишите "статус" чтобы проверить режим самостоятельных уведомлений'
    )


@bot.on.message(text="цетус")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer(message_cetus())


@bot.on.message(text="рассылка")
async def add_to_list_of_chats_in_notify(message: Message):

    group_info = message.peer_id
    if group_info in list_of_chats_in_sleep:
            list_of_chats_in_sleep.remove(group_info)

    if group_info in list_of_chats_in_notify:
        await message.answer("Режим рассылки у вас уже включен")
    else:
        list_of_chats_in_notify.append(group_info)
        await message.answer("Режим рассылки включен")


@bot.on.message(text="ночной режим")
async def add_to_list_of_chats_in_slee(message: Message):

    group_info = message.peer_id
    if group_info in list_of_chats_in_notify:
        list_of_chats_in_notify.remove(group_info)

    if group_info in list_of_chats_in_sleep:
        await message.answer("Ночной режим у вас уже включен")
    else:
        list_of_chats_in_sleep.append(group_info)
        await message.answer("Ночной режим включен")


@bot.on.message(text='статус')
async def check_status(message: Message):
    group_info = message.peer_id

    if group_info in list_of_chats_in_notify:
        await message.answer("Режим рассылки включен")
    else:
        await message.answer("Режим рассылки выключен")


@bot.loop_wrapper.interval(seconds=240)
async def notifications():

    if check_five_min() == 'night':
        for chat in list_of_chats_in_notify:
            await bot.api.messages.send(peer_id=chat, message="ВСЕМ ЕБАТЬ ГЕЙДАЛОНОВ", random_id=0)

    elif check_five_min() == 'day':
        for chat in list_of_chats_in_notify:
            await bot.api.messages.send(peer_id=chat, message="Ночь скоро закончится", random_id=0)


@bot.loop_wrapper.interval(hours=1)
async def status_notification():
    current_hour = datetime.datetime.now()
    if current_hour.hour == 8:
        for chat in list_of_chats_in_sleep:
            await bot.api.messages.send(peer_id=chat, message="Не хотите ли включить рассылку?", random_id=0)

    elif current_hour.hour == 23:
        for chat in list_of_chats_in_notify:
            await bot.api.messages.send(peer_id=chat, message="Не хотите ли выключить рассылку?", random_id=0)


bot.run_forever()


# def get_api_key():
#     return os.environ['API_KEY_SPARLEX']
#
#
# API_token = get_api_key()
#
# list_of_chats_in_notify = []
# list_of_chats_in_sleep = []
#
#
# def chek_sleep():
#     for chat in list_of_chats_in_sleep:
#         vk_session.method('messages.send', {'chat_id': chat, 'message': "Не хотите ли включить режим автоматических уведомлений?", 'random_id': get_random()})
#
#
# def chek_notify():
#     for chat in list_of_chats_in_notify:
#         vk_session.method('messages.send',{'chat_id': chat, 'message': "Не хотите ли включить ночной режим?", 'random_id': get_random()})
#
#
# def for_thr():
#     try:
#         if check_five_min() == 'the night is cooming':
#             for chat in list_of_chats_in_notify:
#                 vk_session.method('messages.send', {'chat_id': chat, 'message': "ВСЕМ ЕБАТЬ ГЕЙДАЛОНОВ", 'random_id': get_random()})
#             threading.Timer(300.0, for_thr).start()
#
#         elif check_five_min() == 'the day is cooming':
#             for chat in list_of_chats_in_notify:
#                 vk_session.method('messages.send', {'chat_id': chat, 'message': "ЕБЛЯ ГЕЙДАЛОНОВ СКОРО ЗАКОНЧИТСя",'random_id': get_random()})
#             threading.Timer(300.0, for_thr).start()
#
#         else:
#             threading.Timer(120.0, for_thr).start()
#
#     except requests.exceptions.ReadTimeout:
#         print("\n Переподключение к серверам ВК \n")
#         time.sleep(3)
#
#
# schedule.every().day.at('08:00').do(chek_sleep)
# schedule.every().day.at('00:00').do(chek_notify)
#
#
# def for_thr_schedule():
#     try:
#         schedule.run_pending()
#         threading.Timer(30.0, for_thr_schedule).start()
#
#     except requests.exceptions.ReadTimeout:
#         print("\n Переподключение к серверам ВК \n")
#         time.sleep(3)
#
#
# vk_session = vk_api.VkApi(token=API_token)
# session_api = vk_session.get_api()
# longpoll = VkBotLongPoll(vk_session, 215538965)
#
#
# try:
#     for event in longpoll.listen():
#
#         if event.type == VkBotEventType.MESSAGE_NEW:
#             response = event.object.message['text'].lower()
#
#             if event.from_chat:
#                 if response == "настройка":
#
#                     for_thr()
#                     for_thr_schedule()
#
#                     if list_of_chats_in_notify.count(event.chat_id) == 0:
#                         list_of_chats_in_notify.append(event.chat_id)
#
#                         if len(list_of_chats_in_sleep) != 0:
#                             list_of_chats_in_sleep.remove(event.chat_id)
#
#                         vk_session.method('messages.send',{'chat_id': event.chat_id, 'message': 'настройка произведена','random_id': get_random()})
#                     else:
#                         vk_session.method('messages.send',{'chat_id': event.chat_id, 'message': 'ваша беседа уже прошла настройку','random_id': get_random()})
#
#                 elif response == "цетус":
#                     vk_session.method('messages.send', {'chat_id':event.chat_id, 'message': message_cetus(), 'random_id': get_random()})
#
#                 elif response == "инфо":
#                     vk_session.method('messages.send',{'chat_id': event.chat_id, 'message':
#                                                         'Привет, я бот, которого сделал жукич.'
#                                                         '\nКак мной пользоваться: '
#                                                         '\n1) напишите "настройка" чтобы настроить самостоятельные уведомления '
#                                                         '\n2) напишите "цетус" чтобы узнать время суток на Цетус'
#                                                         '\n3) напишите "ночной режим" чтобы выключить самостоятельные уведомления'
#                                                         '\n4) напишите "статус" чтобы проверить режим самостоятельных уведомлений',
#                                                        'random_id': get_random()})
#
#                 elif response == "ночной режим":
#                     if list_of_chats_in_sleep.count(event.chat_id) == 0:
#                         list_of_chats_in_sleep.append(event.chat_id)
#
#                         if len(list_of_chats_in_notify) != 0:
#                             list_of_chats_in_notify.remove(event.chat_id)
#
#                         vk_session.method('messages.send', {'chat_id':event.chat_id, 'message': 'ночной режим включён', 'random_id': get_random()})
#                     else:
#                         vk_session.method('messages.send',{'chat_id': event.chat_id, 'message': 'ваша беседа уже в ночном режиме','random_id': get_random()})
#
#                 elif response == "статус":
#                     if event.chat_id in list_of_chats_in_notify:
#                         vk_session.method('messages.send', {'chat_id':event.chat_id, 'message': 'самостоятельные уведомления включены', 'random_id': get_random()})
#                     elif event.chat_id in list_of_chats_in_sleep:
#                         vk_session.method('messages.send', {'chat_id': event.chat_id, 'message': 'самостоятельные уведомления выключены', 'random_id': get_random()})
#                     else:
#                         vk_session.method('messages.send',{'chat_id': event.chat_id, 'message': 'не один из режимов уведомлений не выбран', 'random_id': get_random()})
#
# except requests.exceptions.ReadTimeout:
#         print("\n Переподключение к серверам ВК \n")
#         time.sleep(3)


