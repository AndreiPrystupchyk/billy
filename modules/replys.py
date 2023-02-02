import cache
import random

#billyAnswer
def replyFunc(bot, message, timeStamp):
      bot.send_message(message.chat.id, random.choice(billyReplys), reply_to_message_id=message.id)
      cache.lastBotMessageTime = timeStamp

#pidora answer
def pidoraOtviet(bot, message, timeStamp):
        bot.reply_to(message, random.choice(netAnsers))
        cache.lastBotMessageTime = timeStamp
#yes answer
def daOtvet(bot, message, timeStamp):
    bot.reply_to(message, "Хуй на.🤣")
    cache.lastBotMessageTime = timeStamp
#cs answer
def csOtvet(bot, message, timeStamp):
    bot.reply_to(message, random.choice(csListAnswers))
    cache.lastBotMessageTime = timeStamp

#welcom to the club
def welcomToTheClub(bot,message,timeStamp):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id != bot.user.id:
            bot.send_message(message.chat.id, "Welcome to the club buddy!",reply_to_message_id=message.reply_to_message.message_id)
            cache.lastBotMessageTime = timeStamp
    else:
        bot.send_message(message.chat.id, "Welcome to the club buddy!")
        cache.lastBotMessageTime = timeStamp

#bottle
def sitOnBottle(bot,message,timeStamp):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id != bot.user.id:
            bot.send_message(message.chat.id, random.choice(sitAnswers),reply_to_message_id=message.reply_to_message.message_id)
            cache.lastBotMessageTime = timeStamp
    else:
        bot.send_message(message.chat.id, random.choice(sitAnswers))
        cache.lastBotMessageTime = timeStamp


#ebiot
def ebiot(bot,message,timeStamp):
    bot.reply_to(message, random.choice(ebiotList))
    cache.lastBotMessageTime = timeStamp






#billyAnswer
billyTrigers = [
        'billy',
        'bily',
        'bill',
        'bil',
        'билл',
        'билли',
        'билли,',
        'билли.',
        'билл,'
        'билл.',
        ]

billyReplys = ["Ты чё дерзкий такой?",
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

#pidora answer
pidoraOtvietList = ["нет",
                    "net",
                    "нет.",
                    "net."
                    ]

netAnsers = [
    'Пидора ответ.🤣',
    'Хуй в пакет.',
    'Забайчен',
    'Wasted.',
    'Жизнь тебя ничему не учит...',
    'Есть пробитие.'
    ]

#yes answer
daList = ["da",
          "да",
          "да.",
          "да,",
          "da,",
          "da."
          ]

#cs answer
csListTriger = ["cs",
                "кс",
                "контру",
                "cs.",
                "кс.",
                "контру.",
                "cs,",
                "кс,",
                "контру,",
                "cs?",
                "кс?",
                "контру?"
                ]

csListAnswers = ["Кс для пидоров.",
                 "С нубами не катаю.",
                 "А может в танки?",
                 "Нормальные пацаны в генши играют..."]

#welcom to the club
pidorList = ["пидар",
             "пидор",
             "пидр",
             "pidar",
             "pidor"
             ]

#bottle
bottleList = ["бутылка",
              "бутылку",
              "🍾"
              ]
sitAnswers = [
    "Присел бы...🍾",
    "Что-то я застоялся.🍾",
    "Уфф🍾",
    "Вижу знатока.🍾"
    ]

#ebiot
ebiotList = ["Ебёт?",
             "Ебёт козла?"
             ]

fingersList = ['🤙','👍','👈','👉','👆','🖕','👇','☝']




