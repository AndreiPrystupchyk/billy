import cache
from datetime import datetime
from modules import oai

def checkDate():
    newDate = datetime.now().date()
    day = f'{newDate:%d.%m}'

    for i in range(len(cache.birthdayList)):
        if datetime.strptime(cache.birthdayList[i][3], '%d.%m.%Y').strftime('%d.%m') == day:
            return cache.birthdayList[i]
    else: return False
def happyBirthday(bot, message):
    person = checkDate()
    if person:
        newDate = datetime.now().date()
        year = f'{newDate:%Y}'
        context = f'Сегодня у {person[1]} день рожденья. Поздравь {person[2]} с его праздником в токсично-унизительной манере, ему исполнилось {int(year) - int(datetime.strptime(person[3],"%d.%m.%Y").strftime("%Y"))} лет. Обычно все его называют {person[4]}.'
        oai.birthdayCongrats(bot, message, context)