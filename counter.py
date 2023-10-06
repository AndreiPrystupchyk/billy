import cache
import datetime
import re

date_format = '%d.%m.%Y %H:%M:%S'

def counterGetter(bot,message,isNeedNewCounter):
    messageChatID = message.chat.id
    messageWithoutPrefix = removePrefix(message.text)
    splitedMessage = messageWithoutPrefix.split(',')
    if isNeedNewCounter or isCounterEmpty():
        writeNewCounter(bot,messageChatID,splitedMessage)
    else: 
        readCount(bot,messageChatID)

def removePrefix(input_string):
    pattern = r'^\/[a-zA-Z]+(@[a-zA-Z]+)?\s?'

    match = re.search(pattern, input_string)

    if match:
        modified_string = input_string[len(match.group()):].strip()
    else:
        modified_string = input_string
    return modified_string

def isCounterEmpty():
    if cache.counterData == '' or cache.counterData == []: return True
    else: return False

def checkAreArgsCorrect(splitedMessage):
    if len(splitedMessage) > 2 or len(splitedMessage) < 1:
        return False
    else:
        try:
            if splitedMessage[0] != datetime.datetime.strptime(splitedMessage[0], date_format).strftime(date_format):
                raise ValueError
            return True
        except ValueError:
            return False

def writeNewCounter(bot,chatID,splitedMessage):
    if not checkAreArgsCorrect(splitedMessage):
        bot.send_message(chatID, 'Солнышко, аргументом должна быть дата в формате "dd.mm.YYYY HH:MM:SS" (название ивента опционально после запятой).')
    else:
        cache.counterData = splitedMessage
        readCount(bot,chatID)

def readCount(bot,chatID):
    if not isCounterEmpty():
        counterString = ''
        timenow = datetime.datetime.now().strftime(date_format)
        start = datetime.datetime.strptime(timenow,date_format)
        ends = datetime.datetime.strptime(cache.counterData[0], date_format)
        if len(cache.counterData) > 1:
            counterString = f'{cache.counterData[1]}: {ends - start}'
        else: 
            counterString = f'Осталось: {ends - start}'
        bot.send_message(chatID, counterString)
    else:
        bot.send_message(chatID, 'counter is empty bro :(')

def clearCounterData():
    cache.counterData = ''