import cache
from datetime import datetime
import random

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
    if newHour >= 8:
      return True
    else:
      return False
def checkradarScoreStartingAt():
  if cache.radarScoreStartingAt == '': return False
  else: return True

def gayRadarStart(bot,message,bool):
    if radarCheckDate() and len(cache.chatUsers) > 3:
      newDt = datetime.now().date()
      cache.pidorOfDayDate = newDt
      cache.pidorOfDay = random.choice(cache.chatUsers)
      cache.pidorOfDay['score'] = cache.pidorOfDay['score'] + 1
      defindeAndSayPidorOfDay(bot,message,True)
      day = newDt.strftime('%d.%m.%y')
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
    cache.pinndedMessage = bot.send_message(message.chat.id, f'Похоже пидорас дня сегодня {mention}🥳',parse_mode="Markdown")
    cache.pinndedMessageChatId = cache.pinndedMessage.chat.id
    cache.pinndedMessageId = cache.pinndedMessage.message_id
    bot.pin_chat_message(cache.pinndedMessage.chat.id, cache.pinndedMessage.message_id)
    score(bot,message,False,True)
  else:
    bot.send_message(message.chat.id, f'Пидрила дня сегодня {name}😘')

def score(bot,message,totalMessagesBool, totalRadarBool):
  if checkradarScoreStartingAt():
    statAnswer = f'<b>От {cache.radarScoreStartingAt}:</b>'
    if totalMessagesBool:
      statAnswer += '\n\nВсего сообщений:'
      sortedList = sorted(cache.chatUsers, key=lambda d: d['total_messages'],reverse=True) 
      for i in range(len(sortedList)):
        name = defineName(sortedList[i])
        statAnswer += f'\n<i>{name}: {sortedList[i]["total_messages"]}</i>'
    if totalRadarBool:
      statAnswer += '\n\nГейрадар:'
      sortedList = sorted(cache.chatUsers, key=lambda d: d['score'],reverse=True) 
      for i in range(len(sortedList)):
        name = defineName(sortedList[i])
        statAnswer += f'\n<i>{name}: {sortedList[i]["score"]}</i>'
    bot.send_message(message.chat.id, statAnswer,parse_mode='html')