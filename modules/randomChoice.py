import random
import re

def removePrefix(input_string):
    pattern = r'^\/[a-zA-Z]+(@[a-zA-Z]+)?\s?'

    match = re.search(pattern, input_string)

    if match:
        modified_string = input_string[len(match.group()):].strip()
    else:
        modified_string = input_string

    return modified_string

def getArgs(messageWithoutPrefix):
	return [arg.strip() for arg in messageWithoutPrefix.split(',')]


def randomChoice(bot,message):
	messageWithoutPrefix = removePrefix(message.text)
	args = getArgs(messageWithoutPrefix)
	if args == None or args == ['']:
		bot.send_message(message.chat.id, random.randint(1,100))
	else:
		if len(args) == 1:
			bot.send_message(message.chat.id,'Медвежонок, аргументов должно быть больше одного <3')
		elif len(args) == 2 and args[0].isnumeric() and args[1].isnumeric():
			bot.send_message(message.chat.id,random.randint(int(args[0]),int(args[1])))
		else:
			bot.send_message(message.chat.id,random.choice(args))


