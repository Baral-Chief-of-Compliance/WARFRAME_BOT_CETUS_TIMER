import vk_api, random, time, requests, threading
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import API_token
from datetime import datetime
from parserCetus import get_data_about_cetus
from translator import message_cetus


list_of_chats = []


def get_random():
    value = random.randint(0, 1000000)
    return value

def check_five_min():
    print("проверка начала функции")
    if ((int(datetime.now().strftime('%M')) % 1) == 0):
        print("функция проверки работает")
        info_cetus = get_data_about_cetus()


        if (info_cetus['isDay']):

            time_cetus = info_cetus['timeLeft']
            time_cetus = time_cetus.split(' ')

            if (len(time_cetus) == 2):

                time_m = time_cetus[0]
                time_str = time_m[len(time_m)-1]
                time_m = time_m[:len(time_m)-1]

                if (int(time_m) <= 1 and time_str !='h'):
                    for chat in list_of_chats:
                        vk_session.method('messages.send', {'chat_id': chat, 'message': "ВСЕМ ЕБАТЬ ГЕЙДАЛОНОВ ("+str(time_m)+" мин)", 'random_id': get_random()})


            # elif (len(time_cetus) == 1):
            #     for chat in list_of_chats:
            #         vk_session.method('messages.send', {'chat_id': chat,'message': "ВСЕМ ЕБАТЬ ГЕЙДАЛОНОВ",'random_id': get_random()})

        else:
            time_cetus = info_cetus['timeLeft']
            time_cetus = time_cetus.split(' ')

            if (len(time_cetus) == 2):

                time_m = time_cetus[0]
                time_str = time_m[len(time_m)-1]
                time_m = time_m[:len(time_m)-1]

                if (int(time_m) <= 1 and time_str !='h'):
                    for chat in list_of_chats:
                        vk_session.method('messages.send', {'chat_id': chat, 'message': "ДО КОНЦА НОЧИ МЕНЬШЕ "+str(time_m)+" минут",'random_id': get_random()})

                # elif (len(time_cetus) == 1):
                #     for chat in list_of_chats:
                #         vk_session.method('messages.send', {'chat_id': chat, 'message': "ДО КОНЦА НОЧИ МЕНЬШЕ "+str(time_m)+" МИНУТЫ", 'random_id': get_random()})

def for_thr():
    try:
        threading.Timer(120.0, for_thr).start()
        thread_name = threading.current_thread().name
        print(thread_name)
        print(threading.active_count())
        check_five_min()

    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверам ВК \n")
        time.sleep(3)


vk_session = vk_api.VkApi(token=API_token)
session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 215538965)


try:
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            response = event.object.message['text'].lower()

            if event.from_chat:
                if response == "настройка":

                    for_thr()

                    if list_of_chats.count(event.chat_id) == 0:
                        list_of_chats.append(event.chat_id)
                        vk_session.method('messages.send',{'chat_id': event.chat_id, 'message': 'настройка произведена','random_id': get_random()})
                    else:
                        vk_session.method('messages.send',{'chat_id': event.chat_id, 'message': 'ваша беседа уже прошла настройку','random_id': get_random()})

                elif response == "цетус":
                    print(threading.active_count())
                    vk_session.method('messages.send', {'chat_id':event.chat_id, 'message': message_cetus(), 'random_id': get_random()})

                elif response == "инфо":
                    vk_session.method('messages.send',{'chat_id': event.chat_id, 'message':
                                                                                            'Привет, я бот, которого сделал жукич. '
                                                                                            '\nКак мной пользоваться: '
                                                                                            '\n1) напишите "настройка" чтобы настроить самостоятельные уведомления '
                                                                                            '\n2) напишите "цетус" чтобы узнать время суток на Цетус',
                                                                                            '\n3) напишите "ночной режим" чтобы выключить самостоятельные уведомления'
                                                       'random_id': get_random()})

                elif response == "ночной режим":
                    list_of_chats.remove(event.chat_id)
                    vk_session.method('messages.send', {'chat_id':event.chat_id, 'message': 'ночной режим включён', 'random_id': get_random()})


except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверам ВК \n")
        time.sleep(3)


