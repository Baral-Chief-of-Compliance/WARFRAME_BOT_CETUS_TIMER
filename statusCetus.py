from datetime import datetime
from parserCetus import get_data_about_cetus

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

                if (int(time_m) <= 5 and time_str !='h'):
                    return 'the night is cooming'
                    # for chat in list_of_chats:
                    #     vk_session.method('messages.send', {'chat_id': chat, 'message': "ВСЕМ ЕБАТЬ ГЕЙДАЛОНОВ ("+str(time_m)+" мин)", 'random_id': get_random()})


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

                if (int(time_m) <= 5 and time_str !='h'):
                    return 'the day is cooming'
                    # for chat in list_of_chats:
                    #     vk_session.method('messages.send', {'chat_id': chat, 'message': "ДО КОНЦА НОЧИ МЕНЬШЕ "+str(time_m)+" минут",'random_id': get_random()})

                # elif (len(time_cetus) == 1):
                #     for chat in list_of_chats:
                #         vk_session.method('messages.send', {'chat_id': chat, 'message': "ДО КОНЦА НОЧИ МЕНЬШЕ "+str(time_m)+" МИНУТЫ", 'random_id': get_random()})
