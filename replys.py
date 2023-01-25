import cache
import random

def replyFunc(bot, message, timeStamp):
      bot.send_message(message.chat.id, random.choice(replys), reply_to_message_id=message.id)
      cache.lastBotMessageTime = timeStamp


trigers = [
        'billy',
        'bily',
        'bill',
        'bil',
        'билл',
        'билли'
]

replys = ["Ты чё дерзкий такой?",
    "Выйдём?",
    "Сейчас заламаю...",
    "Пошёл нахуй.",
    "Отсоси мне.",
    "Говна въебал?",
    "Cum...",
    "Dungeon master?",
    "Boss of this gym.",
    "Fucking slave...",
    "Fuck you!",
    "oh shit im sorry",
    "Lets selebrate and suck some dick."
]