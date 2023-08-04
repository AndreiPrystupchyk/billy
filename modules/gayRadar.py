import cache
from datetime import datetime
import random
from modules import oai


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1
def radarCheckDate():
  newDate = datetime.now().date()
  if not checkradarScoreStartingAt():
    cache.radarScoreStartingAt = newDate

  if newDate != cache.pidorOfDayDate:
    return True
  else:
    return False

def radarCheckHour():
    newHour = int(datetime.now().strftime("%H"))
    if newHour >= 6:
      return True
    else:
      return False
    

def checkradarScoreStartingAt():
  if cache.radarScoreStartingAt == '': return False
  else: return True

def gayRadarStart(bot,message,bool):
    if radarCheckDate() and len(cache.chatUsers) > 0:
      priviosPidorOfDay = cache.pidorOfDay
      newDt = datetime.now().date()
      cache.pidorOfDayDate = newDt
      cache.pidorOfDay = random.choice(cache.chatUsers)
      cache.pidorOfDay['score'] = cache.pidorOfDay['score'] + 1
      try:  
        if priviosPidorOfDay['id'] == cache.pidorOfDay['id']:
          cache.pidorOfDay['streak'] += 1
          messageFrom = cache.chatUsers[find(cache.chatUsers,'id',cache.pidorOfDay['id'])]
          messageFrom['pidorStreak'] = cache.pidorOfDay['streak']
        else:
          cache.pidorOfDay['streak'] = 0
      except:
        cache.pidorOfDay['streak'] = 0
      defindeAndSayPidorOfDay(bot,message,True)
    elif bool and cache.pidorOfDay != '':
      defindeAndSayPidorOfDay(bot,message,False)


def defineName(user):
  if user != None or user != '':
    name = ''
    first = user["first_name"]
    last = user["last_name"]
    userN = user["username"]
    if first == None and last == None:
      name = f'{userN}'
    elif first == None:
      name = f'{last}'
    elif last == None:
      name = f'{first}'
    else:
      name = f'{first} {last}'
    return name


def defindeAndSayPidorOfDay(bot,message,bool):
  name = defineName(cache.pidorOfDay)
  if bool:
    mention = f"[{name}](tg://user?id={cache.pidorOfDay['id']})"
    bot.send_message(message.chat.id, 'Запускаю гейрадар. Сейчас посмотрим кто сегодня петушара...')
    try:
      bot.unpin_chat_message(cache.pinndedMessageChatId,cache.pinndedMessageId)
    except:
      print("Can`t unpin")
    if cache.pidorOfDay['streak'] != 0:
      cache.pinndedMessage = bot.send_message(message.chat.id, f'Пидарас дня сегодня {mention}🥳 Идёт со стриком в *{cache.pidorOfDay["streak"]}* подряд! И помни, брат, чем глубже - тем больнее...',parse_mode="markdown")
    else:
      cache.pinndedMessage = bot.send_message(message.chat.id, f'Пидарас дня сегодня {mention}🥳',parse_mode="Markdown")
    cache.pinndedMessageChatId = cache.pinndedMessage.chat.id
    cache.pinndedMessageId = cache.pinndedMessage.message_id
    bot.pin_chat_message(cache.pinndedMessage.chat.id, cache.pinndedMessage.message_id)
    score(bot,message,False,True)
    oai.pdCongrats(bot,message)
  else:
    if cache.pidorOfDay['streak'] != 0:
      bot.send_message(message.chat.id, f'Пидрила дня сегодня {name}😘. Идёт со стриком в *{cache.pidorOfDay["streak"]}* подряд!',parse_mode='markdown')
    else:
      bot.send_message(message.chat.id, f'Пидрила дня сегодня {name}😘')


def score(bot,message,totalMessagesBool, totalRadarBool):
  if checkradarScoreStartingAt():
    statAnswer = f'*От {cache.radarScoreStartingAt}:*'
    if totalRadarBool:
      statAnswer += '\n\n*Гейрадар:*'
      sortedList = sorted(cache.chatUsers, key=lambda d: d['score'],reverse=True) 
      for i in range(len(sortedList)):
        name = defineName(sortedList[i])
        statAnswer += f'\n*{name}: {sortedList[i]["score"]}* (лучший cтрик: _{sortedList[i]["pidorStreak"]}_)'
    if totalMessagesBool:
      statAnswer += '\n\n*Всего сообщений:*'
      sortedList = sorted(cache.chatUsers, key=lambda d: d['total_messages'],reverse=True) 
      for i in range(len(sortedList)):
        name = defineName(sortedList[i])
        statAnswer += f'\n{name}: _{sortedList[i]["total_messages"]}_'
    bot.send_message(message.chat.id, statAnswer,parse_mode='markdown')