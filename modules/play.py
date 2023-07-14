import cache
import modules.steam as steam
from datetime import datetime
import re

################################################# getter

def getter(bot,message,isNeedNewVote,asReply):
  whatGame = determineGame(message,asReply)
  messageId = message.message_id
  messageWithoutPrefix = removePrefix(message.text)
  nameFromWhoMessage = [item for item in cache.telegramList if item.get('tgId') == message.from_user.id][0]['name']
  
  if whatGame == 'Play':
    playSomeThing(bot,message.chat.id,messageId,nameFromWhoMessage,messageWithoutPrefix,isNeedNewVote,whatGame,asReply)
  elif whatGame == 'CS':
    playCs(bot,message.chat.id,messageId,nameFromWhoMessage,messageWithoutPrefix,isNeedNewVote,whatGame,asReply)
  elif whatGame == 'Dota':
    playDota(bot,message.chat.id,messageId,nameFromWhoMessage,messageWithoutPrefix,isNeedNewVote,whatGame,asReply)
    


#################################################

def determineGame(message,asReply):
  if not asReply:
    if message.text.lower().startswith('/play'):
      return 'Play'
    elif message.text.lower().startswith('/cs'):
      return 'CS'
    elif message.text.lower().startswith('/dota'):
      return 'Dota'
  else:
    if any (raport == message.reply_to_message.id for raport in cache.playRaports):
      return 'Play'
    if any (raport == message.reply_to_message.id for raport in cache.csRaports):
      return 'CS'
    if any (raport == message.reply_to_message.id for raport in cache.dotaRaports):
      return 'Dota'
  
#################################################

def removePrefix(input_string):
    pattern = r'^\/[a-zA-Z]+(@[a-zA-Z]+)?\s?'

    match = re.search(pattern, input_string)

    if match:
        modified_string = input_string[len(match.group()):].strip()
    else:
        modified_string = input_string

    return modified_string

#################################################

def playSomeThing(bot,messageChatId,messageId,nameFromWhoMessage,messageWithoutPrefix,isNeedNewVote,whatGame,messageAsReply):
  if isNeedNewVote or cache.playStatus == [] or checkDateForPreviousDay(whatGame):
      cache.playStatus = []
      cache.playRaports = []
      cache.playRaports.append(messageId)
      if messageWithoutPrefix == '':
          pushStatus(whatGame,nameFromWhoMessage,'Катаем во что-нибудь?')
      else:
         pushStatus(whatGame,nameFromWhoMessage,messageWithoutPrefix)
      readRaport(bot,messageChatId,whatGame)
  else:
    if not any (member['name'] == nameFromWhoMessage for member in cache.playStatus) or messageAsReply:
      if messageWithoutPrefix == '':
         pushStatus(whatGame,nameFromWhoMessage,'Катаем во что-нибудь?')
         cache.playRaports.append(messageId)
      else:
        pushStatus(whatGame,nameFromWhoMessage,messageWithoutPrefix)
      readRaport(bot,messageChatId,whatGame)
    else:
      readRaport(bot,messageChatId,whatGame)
   
def playCs(bot,messageChatId,messageId,nameFromWhoMessage,messageWithoutPrefix,isNeedNewVote,whatGame,messageAsReply):
  if isNeedNewVote or cache.csStatus == [] or checkDateForPreviousDay(whatGame):
      cache.csStatus = []
      cache.csRaports = []
      cache.csRaports.append(messageId)
      if messageWithoutPrefix == '':
          pushStatus(whatGame,nameFromWhoMessage,'CS?')
      else:
         pushStatus(whatGame,nameFromWhoMessage,messageWithoutPrefix)
      readRaport(bot,messageChatId,whatGame)
  else:
    if not any (member['name'] == nameFromWhoMessage for member in cache.csStatus) or messageAsReply:
      if messageWithoutPrefix == '':
         pushStatus(whatGame,nameFromWhoMessage,'CS?')
         cache.csRaports.append(messageId)
      else:
        pushStatus(whatGame,nameFromWhoMessage,messageWithoutPrefix)
      readRaport(bot,messageChatId,whatGame)
    else:
      readRaport(bot,messageChatId,whatGame)


def playDota(bot,messageChatId,messageId,nameFromWhoMessage,messageWithoutPrefix,isNeedNewVote,whatGame,messageAsReply):
  if isNeedNewVote or cache.dotaStatus == [] or checkDateForPreviousDay(whatGame):
      cache.dotaStatus = []
      cache.dotaRaports = []
      cache.dotaRaports.append(messageId)
      if messageWithoutPrefix == '':
          pushStatus(whatGame,nameFromWhoMessage,'Dota?')
      else:
         pushStatus(whatGame,nameFromWhoMessage,messageWithoutPrefix)
      readRaport(bot,messageChatId,whatGame)
  else:
    if not any (member['name'] == nameFromWhoMessage for member in cache.dotaStatus) or messageAsReply:
      if messageWithoutPrefix == '':
         pushStatus(whatGame,nameFromWhoMessage,'Dota?')
         cache.dotaRaports.append(messageId)
      else:
        pushStatus(whatGame,nameFromWhoMessage,messageWithoutPrefix)
      readRaport(bot,messageChatId,whatGame)
    else:
      readRaport(bot,messageChatId,whatGame)
   

def readRaport(bot, messageChatId,whatGame):
  respond = ''
  status = ''
  listOfPlayers = ''

  if whatGame == 'Play':
    status = cache.playStatus
    listOfPlayers = [member['name'] for member in cache.telegramList if member['name'] not in cache.playBlackList]
  elif whatGame == 'CS':
     status = cache.csStatus
     listOfPlayers = cache.whoPlayCs
  elif whatGame == 'Dota':
     status = cache.dotaStatus
     listOfPlayers = cache.whoPlayDota
  else:
     print('ReadRaport() cannot be initiated because the game is not defined.')
     return

  now = datetime.now()
  respond += f'*{whatGame}* \n'

  for i in range(len(status)):
    if i == 0:
      respond += f'*{status[i]["name"]}*: {status[i]["status"]} ({datetime.strptime(now.strftime("%H:%M:%S"),"%H:%M:%S") - datetime.strptime(status[i]["time"].strftime("%H:%M:%S"),"%H:%M:%S")} тому) \n'
    else:
       respond += f'\n{status[i]["name"]}: {status[i]["status"]} ({datetime.strptime(now.strftime("%H:%M:%S"),"%H:%M:%S") - datetime.strptime(status[i]["time"].strftime("%H:%M:%S"),"%H:%M:%S")} тому)'

  for ii in range(len(listOfPlayers)):
      if not any(member['name'] == listOfPlayers[ii] for member in status):
          respond += f'\n[{listOfPlayers[ii]}](tg://user?id={[member for member in cache.telegramList if member.get("name") == listOfPlayers[ii]][0]["tgId"]}): ?'
  messageToAppendToRaport = bot.send_message(messageChatId,respond, parse_mode="Markdown")

  if whatGame == 'Play':
    cache.playRaports.append(messageToAppendToRaport.message_id)
  elif whatGame == 'CS':
    cache.csRaports.append(messageToAppendToRaport.message_id)
  elif whatGame == 'Dota':
    cache.dotaRaports.append(messageToAppendToRaport.message_id)

  steam.steamWhoFromSpermobakiOnlineRequest(bot,messageChatId)
  

def pushStatus(whatGame,name,status):
  time = datetime.now()
  if whatGame == 'Play':
    if any(member['name'] == name for member in cache.playStatus):
      for i in range(len(cache.playStatus)):
         if cache.playStatus[i]['name'] == name:
            cache.playStatus[i] = {'name':name,'status':status,'time':time}
    else:
      cache.playStatus.append({'name':name,'status':status,'time':time})
  elif whatGame == 'CS':
    if any(member['name'] == name for member in cache.csStatus):
      for i in range(len(cache.csStatus)):
         if cache.csStatus[i]['name'] == name:
            cache.csStatus[i] = {'name':name,'status':status,'time':time}
    else:
      cache.csStatus.append({'name':name,'status':status,'time':time})
  elif whatGame == 'Dota':
    if any(member['name'] == name for member in cache.dotaStatus):
      for i in range(len(cache.dotaStatus)):
         if cache.dotaStatus[i]['name'] == name:
            cache.dotaStatus[i] = {'name':name,'status':status,'time':time}
    else:
      cache.dotaStatus.append({'name':name,'status':status,'time':time})


def checkDateForPreviousDay(whatGame):
  newDate = datetime.now()
  if whatGame == 'Play':
    if cache.playStatus: 
      if cache.playStatus[0]['time'].date() != newDate.date(): return True
      else: return False
    else: return True
  elif whatGame == 'CS':
    if cache.csStatus: 
      if cache.csStatus[0]['time'].date() != newDate.date(): return True
      else: return False
    else: return True
  elif whatGame == 'Dota':    
    if cache.dotaStatus: 
      if cache.dotaStatus[0]['time'].date() != newDate.date(): return True
      else: return False
    else: return True
  
  
  
  
  if cache.csStatus: 
    if cache.csStatus[0]['time'].date() != newDate.date(): return True
    else: return False
  else: return True

def forceMentionRaport(bot, message):
  whatGame = determineGame(message,False)
  listOfPlayers = ''
  respond = ''
  if whatGame == 'Play':
    listOfPlayers = [member['name'] for member in cache.telegramList if member['name'] not in cache.playBlackList]
    for i in range(len(listOfPlayers)):
      respond += f'\n[{listOfPlayers[i]}](tg://user?id={[member for member in cache.telegramList if member.get("name") == listOfPlayers[i]][0]["tgId"]})'
  elif whatGame == 'CS':
    for i in range(len(cache.whoPlayCs)):
      respond += f'\n[{cache.whoPlayCs[i]}](tg://user?id={[member for member in cache.telegramList if member.get("name") == cache.whoPlayCs[i]][0]["tgId"]})'
  elif whatGame == 'Dota':
    for i in range(len(cache.whoPlayDota)):
      respond += f'\n[{cache.whoPlayDota[i]}](tg://user?id={[member for member in cache.telegramList if member.get("name") == cache.whoPlayDota[i]][0]["tgId"]})'
  else:
     print('forceMentionRaport() cannot be initiated because the game is not defined.')
     return
  bot.send_message(message.chat.id, respond,parse_mode="Markdown")
  steam.steamWhoFromSpermobakiOnlineRequest(bot,message.chat.id)

def addPlayerToList(bot, message):
  whatGame = determineGame(message,False)
  messageWithoutPrefix = removePrefix(message.text).title()
  separetedNames = [name.strip() for name in messageWithoutPrefix.split(',')]
  answer = ''
  userUndefinedInChat = []
  userAlreadyInList = []

  if whatGame == 'Play':
    for i in range(len(separetedNames)):
      if separetedNames[i] in cache.playBlackList:
        userAlreadyInList.append(str(separetedNames[i]))
      else:
        if not separetedNames[i] in list(member["name"] for member in cache.telegramList):
          userUndefinedInChat.append(separetedNames[i])
        else:
          cache.playBlackList.append(separetedNames[i])
    if userUndefinedInChat != [] or userAlreadyInList != []:
        if userUndefinedInChat != []:
            answer += f'Не могу добавить: {", ".join(list(userUndefinedInChat))} \n\nНужно выбрать кого-то из списка: {", ".join(list(member["name"] for member in cache.telegramList))}'
        if userAlreadyInList != []:
            answer += f'\n {", ".join(list(userAlreadyInList))} уже находится в списке.'
        bot.send_message(message.chat.id, answer)
  elif whatGame == 'CS':
    for i in range(len(separetedNames)):
      if separetedNames[i] in cache.whoPlayCs:
        userAlreadyInList.append(str(separetedNames[i]))
      else:
        if not separetedNames[i] in list(member["name"] for member in cache.telegramList):
          userUndefinedInChat.append(separetedNames[i])
        else:
          cache.whoPlayCs.append(separetedNames[i])
    if userUndefinedInChat != [] or userAlreadyInList != []:
        if userUndefinedInChat != []:
            answer += f'Не могу добавить: {", ".join(list(userUndefinedInChat))} \n\nНужно выбрать кого-то из списка: {", ".join(list(member["name"] for member in cache.telegramList))}'
        if userAlreadyInList != []:
            answer += f'\n {", ".join(list(userAlreadyInList))} уже находится в списке.'
        bot.send_message(message.chat.id, answer)
  elif whatGame == 'Dota':
    for i in range(len(separetedNames)):
      if separetedNames[i] in cache.whoPlayDota:
        userAlreadyInList.append(str(separetedNames[i]))
      else:
        if not separetedNames[i] in list(member["name"] for member in cache.telegramList):
          userUndefinedInChat.append(separetedNames[i])
        else:
          cache.whoPlayDota.append(separetedNames[i])
    if userUndefinedInChat != [] or userAlreadyInList != []:
        if userUndefinedInChat != []:
            answer += f'Не могу добавить: {", ".join(list(userUndefinedInChat))} \n\nНужно выбрать кого-то из списка: {", ".join(list(member["name"] for member in cache.telegramList))}'
        if userAlreadyInList != []:
            answer += f'\n {", ".join(list(userAlreadyInList))} уже находится в списке.'
        bot.send_message(message.chat.id, answer)
  else:
    print('addPlayerToList() cannot be initiated because the game is not defined.')
    return
  readListOfPlayers(bot,message,whatGame)


def removePlayerFromList(bot,message):
  whatGame = determineGame(message,False)
  messageWithoutPrefix = removePrefix(message.text).title()
  separetedNames = [name.strip() for name in messageWithoutPrefix.split(',')]
  answer = ''
  userUndefinedInList = []
  if whatGame == 'Play':
    for i in range(len(separetedNames)):
      if not separetedNames[i] in cache.playBlackList:
        userUndefinedInList.append(separetedNames[i])
      else:
        cache.playBlackList.remove(str(separetedNames[i]))
    if userUndefinedInList != []:
        answer += f'\n {", ".join(list(userUndefinedInList))} нету в списке Play.'
        bot.send_message(message.chat.id, answer)
  elif whatGame == 'CS':
    for i in range(len(separetedNames)):
      if not separetedNames[i] in cache.whoPlayCs:
        userUndefinedInList.append(separetedNames[i])
      else:
        cache.whoPlayCs.remove(str(separetedNames[i]))
    if userUndefinedInList != []:
        answer += f'\n {", ".join(list(userUndefinedInList))} нету в списке CS.'
        bot.send_message(message.chat.id, answer)
  elif whatGame == 'Dota':
    for i in range(len(separetedNames)):
      if not separetedNames[i] in cache.whoPlayDota:
        userUndefinedInList.append(separetedNames[i])
      else:
        cache.whoPlayDota.remove(str(separetedNames[i]))
    if userUndefinedInList != []:
        answer += f'\n {", ".join(list(userUndefinedInList))} нету в списке Dota.'
        bot.send_message(message.chat.id, answer)
  else:
     print('csrm() cannot be initiated because the game is not defined.')
     return
  readListOfPlayers(bot,message,whatGame)


def readListOfPlayers(bot,message,whatGame):
  if not whatGame:
    whatGame = determineGame(message, False)
  if whatGame == 'Play':
    bot.send_message(message.chat.id, f'Черный список Play: {", ".join(list(cache.playBlackList))}')
  elif whatGame == 'CS':
    bot.send_message(message.chat.id, f'Белый список CS: {", ".join(list(cache.whoPlayCs))}')
  elif whatGame == 'Dota':
    bot.send_message(message.chat.id, f'Белый список Dota: {", ".join(list(cache.whoPlayDota))}')
  else:
     print('readListOfPlayers() cannot be initiated because the game is not defined.')
     return