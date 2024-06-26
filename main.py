from pathlib import Path
import telebot
import modules.replys as replys
import cache
import config
from datetime import date
import modules.gayRadar as gayRadar
import modules.oai as oai
import modules.play as play
import modules.randomChoice as randomChoice
import modules.counter as counter
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
    cache.gpt4Bool = data['gpt4Bool']
    cache.counterData = data['counterData']

except:
  print("load data error")

def saveCachToDataJson():
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
  cacheToSave['gpt4Bool'] = cache.gpt4Bool
  cacheToSave['counterData'] = cache.counterData
  with open(f'{config.dataPath}/data/data.json', 'w') as outJason:  
    json.dump(cacheToSave, outJason,indent=4, sort_keys=True, default=str)

#################################################
@bot.message_handler(content_types=['voice']) 
def handle_voice(message):
  bot.reply_to(message,'Спасибо за голосовое, петушара.👆',parse_mode='HTML')
#################################################

@bot.message_handler(commands=['vadimpidor']) 
def vadimPidorr(message):
  oai.vadimNahui(bot,message)

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

#################################################     Random

@bot.message_handler(commands=['r','random','R','Random','RANDOM'])
def randomChoiceFunc(message):
  randomChoice.randomChoice(bot,message)

#################################################     Translitterate
@bot.message_handler(commands=['t','transiteration','T'])
def litterate(message):
  transiteration.getter(bot,message)


#@bot.message_handler(commands=['i'])
#def oaiImage(message):
#  oai.oaiImageGenerator(bot,message)
#################################################     

#################################################     Play
@bot.message_handler(commands=['play','Play','PLAY'])
def playGetter(message):
  play.getter(bot, message,isNeedNewVote=False,asReply=False)



@bot.message_handler(commands=['playn','Playn','PLAYN'])
def playNewVote(message):
  play.getter(bot, message,isNeedNewVote=True,asReply=False)

@bot.message_handler(commands=['playm','Playm','PLAYM'])
def playForceMention(message):
  play.forceMentionRaport(bot,message)

@bot.message_handler(commands=['playadd','Playadd','PLAYADD'])
def playAddNewPlayer(message):
  play.addPlayerToList(bot,message)

@bot.message_handler(commands=['playrm','Playrm','PLAYRM'])
def playRemovePlayer(message):
  play.removePlayerFromList(bot, message)

@bot.message_handler(commands=['playlist','Playlist','PLAYLIST'])
def playShowBlackList(message):
  play.readListOfPlayers(bot, message,whatGame=False)

#################################################     CS
@bot.message_handler(commands=['cs','CS','Cs'])
def csCommand(message):
  play.getter(bot, message,isNeedNewVote=False,asReply=False)

@bot.message_handler(commands=['csn','csnew','Csn','CSN','Csnew','CSNEW'])
def csNew(message):
  play.getter(bot, message,isNeedNewVote=True,asReply=False)

@bot.message_handler(commands=['csm','csForceMention','CSM','Csm'])
def csForceMention(message):
  play.forceMentionRaport(bot,message)

@bot.message_handler(commands=['csadd'])
def csadduser(message):
  play.addPlayerToList(bot,message)

@bot.message_handler(commands=['csrm','csremove'])
def csremove(message):
  play.removePlayerFromList(bot, message)

@bot.message_handler(commands=['cslist'])
def csshowlist(message):
  play.readListOfPlayers(bot, message,whatGame=False)
################################################# Dota
@bot.message_handler(commands=['dota','Dota','DOTA'])
def dotaCommand(message):
  play.getter(bot, message,isNeedNewVote=False,asReply=False)

@bot.message_handler(commands=['dotan','dotanew','Dotan','DOTAN'])
def dotaNew(message):
  play.getter(bot, message,isNeedNewVote=True,asReply=False)

@bot.message_handler(commands=['dotam','dotaForceMention','Dotam','DOTAM'])
def dotaForceMention(message):
  play.forceMentionRaport(bot,message)

@bot.message_handler(commands=['dotaadd'])
def dotaadduser(message):
  play.addPlayerToList(bot,message)

@bot.message_handler(commands=['dotarm','dotaremove'])
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

@bot.message_handler(commands=['smart4'])
def oai4Toggle(message):
  if message.from_user.id == andreiID:
    cache.gpt4Bool = not cache.gpt4Bool
    bot.send_message(message.chat.id, f'GPT4: {cache.gpt4Bool}')

@bot.message_handler(commands=['historyLimit'])
def historyLim(message):
  if message.from_user.id == andreiID:
    cache.historyLimit = int(message.text.lower().replace('/historylimit ', ''))
    bot.send_message(message.chat.id, f'historyLimit: {cache.historyLimit}')

@bot.message_handler(commands=['n','newrequestopenai'])
def smrt(message):
  if cache.openaiToggle:
    oai.dequeLenOperator(True)
    oai.oaiMessageGetter(bot, message,True)
  else:
    bot.send_message(message.chat.id, 'Функция отключена ;(')


@bot.message_handler(commands=['4','gpt4'])
def gpt4Model(message):
  if cache.gpt4Bool:
    oai.gpt4(bot, message)
  else:
    bot.send_message(message.chat.id, 'Функция отключена ;(')

@bot.message_handler(commands=['counter','c'])
def counterFunc(message):
  counter.counterGetter(bot,message,False)

@bot.message_handler(commands=['counterNew','cn'])
def counterNewFunc(message):
  counter.counterGetter(bot,message,True)

@bot.message_handler(commands=['counterReset','cr'])
def clearCounter(message):
  counter.clearCounterData()


#################################################
def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1
#################################################

#################################################
@bot.message_handler(commands=['statReset'])
def statsReset(message):
  if message.from_user.id == andreiID:
    bot.unpin_chat_message(cache.pinndedMessageChatId,cache.pinndedMessageId)
    cache.pinndedMessageChatId = ''
    cache.pinndedMessageId = ''
    cache.radarScoreStartingAt = ''
    cache.pidorOfDay = ''
    cache.pidorOfDayDate = ''
    for i in range(len(cache.chatUsers)):
      cache.chatUsers[i]['score'] = 0
      cache.chatUsers[i]['total_messages'] = 0
      cache.chatUsers[i]['pidorStreak'] = 0
    saveCachToDataJson()
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

  if message.text.lower().startswith('@spermobakibot'):
    oai.oaiMessageGetter(bot,message,True)
    answer = False
  
  if message.reply_to_message:
    if any(messageId == message.reply_to_message.id for messageId in (cache.playRaports + cache.csRaports + cache.dotaRaports)):
        play.getter(bot,message,isNeedNewVote=False,asReply=True)
        answer = False

    if message.reply_to_message.from_user.id == bot.user.id and answer:
      if cache.openaiToggle:
        if len(oai.botHistory) == 0 or cache.historyLimit == 0:
          oai.oaiMessageGetter(bot,message,True)
          answer = False
        else:
          oai.oaiMessageGetter(bot,message,False)
          answer = False
      else:
          if message.reply_to_message.text == 'Хуй на.🤣':
            bot.reply_to(message, "Возьми два.🤣🤣🤣")
          else:
            personalAnswer = random.randint(1,3)
            if personalAnswer == 1:
              nameFromWhoMessage = [item for item in cache.telegramList if item.get('tgId') == message.from_user.id][0]['name']
              bot.send_message(message.chat.id, f'Ай, {nameFromWhoMessage}, иди нахуй.', reply_to_message_id=message.id)
              answer = False
            else:
              replys.replyFunc(bot,message)
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



  saveCachToDataJson()

bot.polling(non_stop=True)
