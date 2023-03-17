import cache

def csSend(bot, message):
    args = message.text.lower()
    csAskList = []
    if args == '/cs':
        csAsk = 'Будете в кс?\n\n'
    else:
        csAsk = args.removeprefix('/cs ')
        csAsk += '\n\n'
    for i in range(len(cache.whoPlayCs)):
        mentionToAsk = f"[{cache.whoPlayCs[i]}](tg://user?id={cache.spermachiList[cache.whoPlayCs[i]]})"
        csAskList.append(mentionToAsk)
    csAsk += ', '.join(list(csAskList))
    bot.send_message(message.chat.id, csAsk,parse_mode="Markdown")

def csadd(bot, message):
    m = message.text.lower().removeprefix('/csadd').title()
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
            answer += f'\n {", ".join(list(noInChat))} уже находится в списке.'
        bot.send_message(message.chat.id, answer)
    cslist(bot,message)



def csrm(bot,message):
    m = message.text.lower().removeprefix('/csrm').title()
    args = [x.strip() for x in m.split(',')]
    answer = ''
    noInList = []
    for i in range(len(args)):
      if not args[i] in cache.whoPlayCs:
        noInList.append(args[i])
      else:
        cache.whoPlayCs.remove(str(args[i]))
    if noInList != []:
        answer += f'\n {", ".join(list(noInList))} нету в списке нубов.'
        bot.send_message(message.chat.id, answer)
    cslist(bot,message)
  
def cslist(bot,message):
    bot.send_message(message.chat.id, f'Список спермачей: {", ".join(list(cache.whoPlayCs))}')