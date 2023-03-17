#pingwinka
import telebot
import modules.replys as replys
import cache
import config
import time
from datetime import datetime, date
import modules.gayRadar as gayRadar
import modules.randomVoice as randomVoice
import modules.cs as cs
import random
import json


API_KEY = config.token
bot = telebot.TeleBot(API_KEY)
bot.set_webhook()

andreiID = 355407137

try:
  with open (f'{config.dataPath}/data/data.json','r+') as dataFile:
    data = json.loads(dataFile.read())
    cache.lastBotMessageTime = data['lastBotMessageTime']
    cache.botTimeOut = data['botTimeOut']
    cache.pidorOfDay = data['pidorOfDay']
    cache.pidorOfDayDate = date.fromisoformat(data['pidorOfDayDate'])
    cache.radarScoreStartingAt = date.fromisoformat(data['radarScoreStartingAt'])
    cache.chatUsers = data['chatUsers']
    cache.pinndedMessageId  = int(data['pinndedMessageId'])
    cache.pinndedMessageChatId  = int(data['pinndedMessageChatId'])
    cache.whoPlayCs = data['whoPlayCs']
except:
  print("load data error")

#################################################
@bot.message_handler(content_types=['voice']) 
def handle_voice(message):
  bot.reply_to(message,'Спасибо за голосовое, петушара.👆',parse_mode='HTML')
#################################################
@bot.message_handler(content_types=["new_chat_members"])
def foo(message):
  tempDateStamp = int(time.time())
  replys.welcomToTheClub(bot,message,tempDateStamp)
#################################################
@bot.message_handler(commands=['radar'])
def radar(message):
  gayRadar.gayRadarStart(bot,message, True)
#################################################
@bot.message_handler(commands=['stat'])
def radar(message):
  gayRadar.score(bot,message, True, True)


#################################################     CS
@bot.message_handler(commands=['cs'])
def csCommand(message):
  cs.csSend(bot, message)

@bot.message_handler(commands=['csadd'])
def csadduser(message):
  cs.csadd(bot, message)

@bot.message_handler(commands=['csrm'])
def csremove(message):
  cs.csrm(bot, message)

@bot.message_handler(commands=['cslist'])
def csshowlist(message):
  cs.cslist(bot, message)

#################################################
@bot.message_handler(commands=['radarReset'])
def radarReset(message):
  if message.from_user.id == andreiID:
    cache.pidorOfDay = ''
    cache.pidorOfDayDate = ''
    bot.unpin_chat_message(cache.pinndedMessageChatId,cache.pinndedMessageId)
    cache.pinndedMessageId = ''
    cache.pinndedMessageChatId = ''
    bot.send_message(message.chat.id, 'Ты опустошил мой бак...')
#################################################
def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1
#################################################
@bot.message_handler(commands=['statReset'])
def radarReset(message):
  cache.radarScoreStartingAt = ''
  cache.pidorOfDay = ''
  cache.pidorOfDayDate = ''
  if message.from_user.id == andreiID:
    for i in range(len(cache.chatUsers)):
      cache.chatUsers[i]['score'] = 0
    for i in range(len(cache.chatUsers)):
      cache.chatUsers[i]['total_messages'] = 0
    bot.send_message(message.chat.id, 'Ты опустошил мой бак...')

#################################################
@bot.message_handler()
def handle_message(message):
  tempDateStamp = int(time.time())
  answer = True
  if len(cache.chatUsers) < 7:
    if message.from_user.id != bot.user.id:
      if not any(d['id'] == message.from_user.id for d in cache.chatUsers):
        cache.chatUsers.append({'id':message.from_user.id,'username':message.from_user.username,'first_name':message.from_user.first_name,'last_name':message.from_user.last_name,'score':0,'total_messages':0})
  if cache.chatUsers != '':
    messageFromUser = ''
    messageFromUser = cache.chatUsers[find(cache.chatUsers,'id',message.from_user.id)]
    messageFromUser['total_messages'] = messageFromUser['total_messages'] + 1

  if gayRadar.radarCheckDate() and gayRadar.radarCheckHour():
    gayRadar.gayRadarStart(bot, message, False)
  
  if message.date - cache.lastBotMessageTime > cache.botTimeOut:
    if message.reply_to_message:
#################################################   #agro answer

      if message.reply_to_message.from_user.id == bot.user.id:
        if message.reply_to_message.text == 'Хуй на.🤣':
          bot.reply_to(message, "Возьми два.🤣🤣🤣")
          cache.lastBotMessageTime = tempDateStamp
        else:
          personalAnswer = random.randint(1,3)
          if personalAnswer == 1:
            name = list(cache.spermachiList.keys())[list(cache.spermachiList.values()).index(message.from_user.id)]
            bot.send_message(message.chat.id, f'Ай, {name}, иди нахуй.', reply_to_message_id=message.id)
            cache.lastBotMessageTime = tempDateStamp
          else:
            replys.replyFunc(bot,message,tempDateStamp)
      else:
        replys.replyFunc(bot,message,tempDateStamp)
        answer = False
#################################################   #billy triger
    if answer and any(ext in message.text.lower() for ext in replys.billyTrigers):
      replys.replyFunc(bot,message,tempDateStamp)
      answer = False
#################################################   #pidora otvet
    if answer and message.text.lower() in replys.pidoraOtvietList:
      replys.pidoraOtviet(bot,message,tempDateStamp)
      answer = False
#################################################   #huina
    if answer and message.text.lower() in replys.daList:
      replys.daOtvet(bot,message,tempDateStamp)
      answer = False
#################################################   #cs
    if answer and (any(ext in message.text.lower() for ext in replys.csListTriger) or message.text.lower() == 'кс?'):
      replys.csOtvet(bot,message,tempDateStamp)
      answer = False
#################################################   #palec
    if answer and any(ext in message.text for ext in replys.fingersList):
      bot.reply_to(message,'Ох, блять, какой палец, его бы мне в жопу...')
      cache.lastBotMessageTime = tempDateStamp
      answer = False
#################################################   #welcomeToTheClub pidor
    if answer and any(ext in message.text.lower() for ext in replys.pidorList):
      replys.welcomToTheClub(bot,message,tempDateStamp)
      answer = False
#################################################   #bottle
    if answer and any(ext in message.text.lower() for ext in replys.bottleList):
      replys.sitOnBottle(bot,message,tempDateStamp)
      answer = False
    
#################################################   #celebrate
    if answer and "@Spermobakibot" in message.text:
      bot.send_message(message.chat.id, "Let's celebrate and suck some dick!")
      cache.lastBotMessageTime = tempDateStamp
      answer = False
#################################################   #voice
    if answer and (random.randint(1,70) == 69):
      randomVoice.randomVoicePlay(bot,message)
      answer = False
#################################################    #ebiot?
    if answer and message.text.endswith('?') and random.randint(1,13) == 1:
      replys.ebiot(bot,message,tempDateStamp)
  

  cacheToSave = {}
  cacheToSave['lastBotMessageTime'] = cache.lastBotMessageTime
  cacheToSave['botTimeOut'] = cache.botTimeOut
  cacheToSave['pidorOfDay'] = cache.pidorOfDay
  cacheToSave['pidorOfDayDate'] = cache.pidorOfDayDate
  cacheToSave['radarScoreStartingAt'] = cache.radarScoreStartingAt
  cacheToSave['chatUsers'] = cache.chatUsers 
  cacheToSave['pinndedMessageId'] = cache.pinndedMessageId
  cacheToSave['pinndedMessageChatId'] = cache.pinndedMessageChatId
  cacheToSave['whoPlayCs'] = cache.whoPlayCs
  with open(f'{config.dataPath}/data/data.json', 'w') as outJason:  
    json.dump(cacheToSave, outJason,indent=4, sort_keys=True, default=str)

bot.polling(non_stop=True)
