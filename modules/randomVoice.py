import os
import random

cwd = os.getcwd()
listOfAudio = f'{cwd}/audio/'
numberOfFiles = 3

def randomVoicePlay(bot,message):
    voice = open(f'{cwd}/audio/{random.randint(1,numberOfFiles)}.ogg','rb')
    bot.send_voice(message.chat.id, voice=voice)
