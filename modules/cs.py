import cache
from datetime import datetime


#################################################
def removeBotName(str):
  return str.text.lower().replace('/cs@spermobakibot', '/cs')

def readRaport(bot, message):
  respond = ''
  now = datetime.now()
  for i in range(len(cache.csStatus)):
    if i == 0:
      respond += f'***{cache.csStatus[i]["name"]}: {cache.csStatus[i]["status"]} ({datetime.strptime(now.strftime("%H:%M:%S"),"%H:%M:%S") - datetime.strptime(cache.csStatus[i]["time"].strftime("%H:%M:%S"),"%H:%M:%S")} назад)***'
      respond += '\n'
    else:
       respond += f'\n{cache.csStatus[i]["name"]}: {cache.csStatus[i]["status"]} ({datetime.strptime(now.strftime("%H:%M:%S"),"%H:%M:%S") - datetime.strptime(cache.csStatus[i]["time"].strftime("%H:%M:%S"),"%H:%M:%S")} назад)'

  for ii in range(len(cache.whoPlayCs)):
     if not any(m['name'] == cache.whoPlayCs[ii] for m in cache.csStatus):
        respond += f'\n[{cache.whoPlayCs[ii]}](tg://user?id={cache.spermachiList[cache.whoPlayCs[ii]]}): ?'
  messToRaport = bot.send_message(message.chat.id, respond, parse_mode="Markdown")
  cache.raports.append(messToRaport.message_id)
        

def pushStatus(name,status,time):
   if any(m['name'] == name for m in cache.csStatus):
      for i in range(len(cache.csStatus)):
         if cache.csStatus[i]['name'] == name:
            cache.csStatus[i] = {'name':name,'status':status,'time':time}

   else:
      cache.csStatus.append({'name':name,'status':status,'time':time})

def checkDate():
  newDate = datetime.now()
  if cache.csStatus: 
    if cache.csStatus[0]['time'].date() != newDate.date(): return True
    else: return False
  else: return True


def csReq(bot, message, isNeedNew):
    mes = removeBotName(message)
    fromWho = list(cache.spermachiList.keys())[list(cache.spermachiList.values()).index(message.from_user.id)]
    now = datetime.now()
    if isNeedNew or checkDate():
      cache.csStatus = []
      cache.raports = []
      if mes == '/cs':
          pushStatus(fromWho,'Будете в кс?',now)
      else:
          if mes == '/csn':
             pushStatus(fromWho,'Будете в кс?',now)
          else:
            m = mes.removeprefix('/csn ')
            m = m.removeprefix('/cs ')
            pushStatus(fromWho,m,now)
      readRaport(bot, message)
    else:
      if message.text == '/cs':
         readRaport(bot, message)
      else:
        m = mes.removeprefix('/cs')
        pushStatus(fromWho,m,now)
        readRaport(bot, message)
        
         

def csadd(bot, message):
    mes = removeBotName(message).lower()
    m = mes.removeprefix('/csadd').title()
    args = [x.strip() for x in m.split(',')]
    answer = ''
    noInChat = []
    alreadyInList = []
    for i in range(len(args)):
      if args[i] in cache.whoPlayCs:
        alreadyInList.append(str(args[i]))
      else:
        if not args[i] in cache.spermachiList.keys():
          noInChat.append(args[i])
        else:
          cache.whoPlayCs.append(args[i])
    if noInChat != [] or alreadyInList != []:
        if noInChat != []:
            answer += f'Не могу добавить: {", ".join(list(noInChat))} \n\nНужно выбрать кого-то из списка: {", ".join(list(cache.spermachiList.keys()))}'
        if alreadyInList != []:
            answer += f'\n {", ".join(list(alreadyInList))} уже находится в списке.'
        bot.send_message(message.chat.id, answer)
    cslist(bot,message)



def csrm(bot,message):
    mes = removeBotName(message).lower()
    m = mes.removeprefix('/csrm').title()
    args = [x.strip() for x in m.split(',')]
    answer = ''
    noInList = []
    for i in range(len(args)):
      if not args[i] in cache.whoPlayCs:
        noInList.append(args[i])
      else:
        cache.whoPlayCs.remove(str(args[i]))
    if noInList != []:
        answer += f'\n {", ".join(list(noInList))} нету в списке баков.'
        bot.send_message(message.chat.id, answer)
    cslist(bot,message)
  
def cslist(bot,message):
    bot.send_message(message.chat.id, f'Список спермачей: {", ".join(list(cache.whoPlayCs))}')