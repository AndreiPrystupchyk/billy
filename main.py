from pathlib import Path
import telebot
import modules.replys as replys
import cache
import config
from datetime import date
import modules.gayRadar as gayRadar
import modules.oai as oai
import modules.play as play
import random
import json
import modules.steam as steam
import modules.transiteration as transiteration

tgToken = config.token
bot = telebot.TeleBot(tgToken)
bot.set_webhook()

andreiID = cache.andreiID

try:
  my_file = Path(f'{config.dataPath}/data/data.json')
  with open (f'{config.dataPath}/data/data.json','r+') as dataFile:
    data = json.loads(dataFile.read())
    cache.pidorOfDay = data['pidorOfDay']
    cache.pidorOfDayDate = date.fromisoformat(data['pidorOfDayDate'])
    cache.radarScoreStartingAt = date.fromisoformat(data['radarScoreStartingAt'])
    cache.chatUsers = data['chatUsers']
    cache.pinndedMessageId  = int(data['pinndedMessageId'])
    cache.pinndedMessageChatId  = int(data['pinndedMessageChatId'])
    cache.whoPlayCs = data['whoPlayCs']
    cache.whoPlayDota = data['whoPlayDota']
    cache.playBlackList = data['playBlackList']
    cache.openaiToggle = data['openaiToggle']
    cache.historyLimit = int(data['historyLimit'])

except:
  print("load data error")

#################################################
@bot.message_handler(content_types=['voice']) 
def handle_voice(message):
  bot.reply_to(message,'Спасибо за голосовое, петушара.👆',parse_mode='HTML')
#################################################
@bot.message_handler(commands=['newChatMember'])
def newMember(message):
  addNewUser(message)
#################################################
@bot.message_handler(commands=['radar'])
def radar(message):
  gayRadar.gayRadarStart(bot,message, True)
#################################################
@bot.message_handler(commands=['stat'])
def radarStat(message):
  gayRadar.score(bot,message, True, True)
#################################################
@bot.message_handler(commands=['backup'])
def backup(message):
  if message.from_user.id == andreiID:
    with open (f'{config.dataPath}/backup/data.json','r') as dataFile:
      data = json.loads(dataFile.read())
      cache.pidorOfDay = data['pidorOfDay']
      cache.pidorOfDayDate = date.fromisoformat(data['pidorOfDayDate'])
      cache.radarScoreStartingAt = date.fromisoformat(data['radarScoreStartingAt'])
      cache.chatUsers = data['chatUsers']
      #cache.pinndedMessageId  = int(data['pinndedMessageId'])
      #cache.pinndedMessageChatId  = int(data['pinndedMessageChatId'])
      cache.openaiToggle = data['openaiToggle']
      cache.whoPlayCs = data['whoPlayCs']
#################################################     Steam

@bot.message_handler(commands=['steam'])
def SteamRequest(message):
  steam.steamWhoFromSpermobakiOnlineRequest(bot,message.chat.id)

#################################################     Translitterate
@bot.message_handler(commands=['t'])
def litterate(message):
  transiteration.getter(bot,message)
#################################################     P
@bot.message_handler(commands=['p'])
def handle_play(message):
  user_markup = telebot.types.ReplyKeyboardMarkup(True,False)
  user_markup = telebot.types.ReplyKeyboardMarkup()
  user_markup.row ('/play')
  user_markup.row ('/CS','/Dota')
  user_markup.row ('/cancel')
  bot.send_message(message.chat.id,'Play',reply_markup=user_markup)

@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
  hide_markup = telebot.types.ReplyKeyboardRemove()
  bot.send_message(message.chat.id,'..', reply_markup=hide_markup)
#################################################     Play
@bot.message_handler(commands=['play'])
def playGetter(message):
  play.getter(bot, message,isNeedNewVote=False,asReply=False)

@bot.message_handler(commands=['playn'])
def playNewVote(message):
  play.getter(bot, message,isNeedNewVote=True,asReply=False)

@bot.message_handler(commands=['playm'])
def playForceMention(message):
  play.forceMentionRaport(bot,message)

@bot.message_handler(commands=['playadd'])
def playAddNewPlayer(message):
  play.addPlayerToList(bot,message)

@bot.message_handler(commands=['playrm'])
def playRemovePlayer(message):
  play.removePlayerFromList(bot, message)

@bot.message_handler(commands=['playlist'])
def playShowBlackList(message):
  play.readListOfPlayers(bot, message,whatGame=False)

#################################################     CS
@bot.message_handler(commands=['cs'])
def csCommand(message):
  play.getter(bot, message,isNeedNewVote=False,asReply=False)

@bot.message_handler(commands=['csn'])
def csNew(message):
  play.getter(bot, message,isNeedNewVote=True,asReply=False)

@bot.message_handler(commands=['csm'])
def csForceMention(message):
  play.forceMentionRaport(bot,message)

@bot.message_handler(commands=['csadd'])
def csadduser(message):
  play.addPlayerToList(bot,message)

@bot.message_handler(commands=['csrm'])
def csremove(message):
  play.removePlayerFromList(bot, message)

@bot.message_handler(commands=['cslist'])
def csshowlist(message):
  play.readListOfPlayers(bot, message,whatGame=False)
################################################# Dota
@bot.message_handler(commands=['dota'])
def dotaCommand(message):
  play.getter(bot, message,isNeedNewVote=False,asReply=False)

@bot.message_handler(commands=['dotan'])
def dotaNew(message):
  play.getter(bot, message,isNeedNewVote=True,asReply=False)

@bot.message_handler(commands=['dotam'])
def dotaForceMention(message):
  play.forceMentionRaport(bot,message)

@bot.message_handler(commands=['dotaadd'])
def dotaadduser(message):
  play.addPlayerToList(bot,message)

@bot.message_handler(commands=['dotarm'])
def dotaremove(message):
  play.removePlayerFromList(bot, message)

@bot.message_handler(commands=['dotalist'])
def dotashowlist(message):
  play.readListOfPlayers(bot, message,whatGame=False)
#################################################
@bot.message_handler(commands=['smart'])
def oaiToggle(message):
  if message.from_user.id == andreiID:
    cache.openaiToggle = not cache.openaiToggle
    bot.send_message(message.chat.id, f'OpenAI Billy: {cache.openaiToggle}')

@bot.message_handler(commands=['historyLimit'])
def historyLim(message):
  if message.from_user.id == andreiID:
    cache.historyLimit = int(message.text.lower().replace('/historylimit ', ''))
    bot.send_message(message.chat.id, f'historyLimit: {cache.historyLimit}')

@bot.message_handler(commands=['n'])
def smrt(message):
  if cache.openaiToggle:
    oai.dequeLenOperator(True)
    oai.oaiMessageGetter(bot, message,True)
  else:
    bot.send_message(message.chat.id, 'Функция отключена ;(')

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
################################################# pidor streak 0
@bot.message_handler(commands=['pidorstreak'])
def pds(message):
  if message.from_user.id == andreiID:
    for i in range(len(cache.chatUsers)):
      cache.chatUsers[i]['pidorStreak'] = 0
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
    for i in range(len(cache.chatUsers)):
      cache.chatUsers[i]['pidorStreak'] = 0
    bot.send_message(message.chat.id, 'Ты опустошил мой бак...')
#################################################
@bot.message_handler(commands=['renameme'])
def rename(message):
      user = cache.chatUsers[find(cache.chatUsers,'id',message.from_user.id)]
      user['username'] = message.from_user.username
      user['first_name'] = message.from_user.first_name
      user['last_name'] = message.from_user.last_name
      bot.send_message(message.chat.id, f'Твоё новое имя: {gayRadar.defineName(user)}')
def addNewUser(message):
  if message.reply_to_message:
    q = message.reply_to_message
    if q.id != bot.user.id:
      if not any(d['id'] == q.id for d in cache.chatUsers):
        cache.chatUsers.append({'id':q.id,'username':q.from_user.username,'first_name':q.from_user.first_name,'last_name':q.from_user.last_name,'score':0,'total_messages':0,'pidorStreak':0})
        replys.welcomToTheClub(bot,message)      
      else:
        bot.send_message(message.chat.id, 'Он здесь уже давно :D')
    else:
      bot.send_message(message.chat.id, 'Не меня же, даун xD')
  else:
    bot.send_message(message.chat.id, 'Процитируй новичка, пупсик :*')
#################################################
@bot.message_handler()
def handle_message(message):
  answer = True
  if len(cache.chatUsers) != 0:
    messageFromUser = ''
    messageFromUser = cache.chatUsers[find(cache.chatUsers,'id',message.from_user.id)]
    messageFromUser['total_messages'] = messageFromUser['total_messages'] + 1

  if gayRadar.radarCheckDate() and gayRadar.radarCheckHour():
    gayRadar.gayRadarStart(bot, message, False)

  
  if message.reply_to_message:
    if any(messageId == message.reply_to_message.id for messageId in (cache.playRaports + cache.csRaports + cache.dotaRaports)):
        play.getter(bot,message,isNeedNewVote=False,asReply=True)
        answer = False

#################################################   #billy triger
    if answer and any(ext in message.text.lower() for ext in replys.billyTrigers):
          replys.replyFunc(bot,message)
          answer = False
#################################################   #pidora otvet
    if answer and message.text.lower() in replys.pidoraOtvietList:
      replys.pidoraOtviet(bot,message)
      answer = False
#################################################   #huina
    if answer and message.text.lower() in replys.daList:
      replys.daOtvet(bot,message)
      answer = False
#################################################   #cs
    if answer and (any(ext in message.text.lower() for ext in replys.csListTriger) or message.text.lower() == 'кс?'):
      replys.csOtvet(bot,message)
      answer = False
#################################################   #palec
    if answer and any(ext in message.text for ext in replys.fingersList):
      bot.reply_to(message,'Ох, блять, какой палец, его бы мне в жопу...')
      answer = False
#################################################   #welcomeToTheClub pidor
    if answer and any(ext in message.text.lower() for ext in replys.pidorList):
      replys.welcomToTheClub(bot,message)
      answer = False
#################################################   #bottle
    if answer and any(ext in message.text.lower() for ext in replys.bottleList):
      replys.sitOnBottle(bot,message)
      answer = False
    
#################################################   #celebrate
    if answer and "@Spermobakibot" in message.text:
      bot.send_message(message.chat.id, "Let's celebrate and suck some dick!")
      answer = False

#################################################    #ebiot?
    if answer and message.text.endswith('?') and random.randint(1,12) == 1:
      replys.ebiot(bot,message)
  

  cacheToSave = {}
  cacheToSave['pidorOfDay'] = cache.pidorOfDay
  cacheToSave['pidorOfDayDate'] = cache.pidorOfDayDate
  cacheToSave['radarScoreStartingAt'] = cache.radarScoreStartingAt
  cacheToSave['chatUsers'] = cache.chatUsers 
  cacheToSave['pinndedMessageId'] = cache.pinndedMessageId
  cacheToSave['pinndedMessageChatId'] = cache.pinndedMessageChatId
  cacheToSave['whoPlayCs'] = cache.whoPlayCs
  cacheToSave['whoPlayDota'] = cache.whoPlayDota
  cacheToSave['playBlackList'] = cache.playBlackList
  cacheToSave['openaiToggle'] = cache.openaiToggle
  cacheToSave['historyLimit'] = cache.historyLimit

  with open(f'{config.dataPath}/data/data.json', 'w') as outJason:  
    json.dump(cacheToSave, outJason,indent=4, sort_keys=True, default=str)


bot.polling(non_stop=True)
