from parserCetus import get_data_about_cetus


def message_cetus():
    info_cetus = get_data_about_cetus()
    if info_cetus['isDay']:
        responce = 'сейчас на Цетус день до ночи осталось: ' + str(info_cetus['timeLeft'])
    else:
        responce = 'сейчас на Цетусе ночь до дня осталось: ' +str(info_cetus['timeLeft'])

    return responce
