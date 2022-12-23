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
                    return 'night'

        else:
            time_cetus = info_cetus['timeLeft']
            time_cetus = time_cetus.split(' ')

            if (len(time_cetus) == 2):

                time_m = time_cetus[0]
                time_str = time_m[len(time_m)-1]
                time_m = time_m[:len(time_m)-1]

                if (int(time_m) <= 5 and time_str !='h'):
                    return 'day'