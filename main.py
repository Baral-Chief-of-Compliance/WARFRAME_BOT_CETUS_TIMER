import vk_api, time, requests, threading, schedule, datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from translator import message_cetus
from statusCetus import check_five_min
from randomChatId import get_random
import os
import asyncio
from vkbottle import Keyboard, Text
import logging
from config import API_token
from vkbottle.bot import Bot, Message


bot = Bot(token=API_token)
bot.labeler.vbml_ignore_case = True


@bot.on.message(text="цетус")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Пошел нахуй, {}".format(users_info[0].first_name))

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


