import cache
import random

#billyAnswer
def replyFunc(bot, message):
      bot.send_message(message.chat.id, random.choice(billyReplys), reply_to_message_id=message.id)

#pidora answer
def pidoraOtviet(bot, message):
        bot.reply_to(message, random.choice(netAnsers))

#yes answer
def daOtvet(bot, message):
    bot.reply_to(message, "Хуй на.🤣")

#cs answer
def csOtvet(bot, message):
    bot.reply_to(message, random.choice(csListAnswers))


#welcom to the club
def welcomToTheClub(bot,message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id != bot.user.id:
            bot.send_message(message.chat.id, "Welcome to the club buddy!",reply_to_message_id=message.reply_to_message.message_id)

    else:
        bot.send_message(message.chat.id, "Welcome to the club buddy!")


#bottle
def sitOnBottle(bot,message,):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id != bot.user.id:
            bot.send_message(message.chat.id, random.choice(sitAnswers),reply_to_message_id=message.reply_to_message.message_id)

    else:
        bot.send_message(message.chat.id, random.choice(sitAnswers))



#ebiot
def ebiot(bot,message):
    bot.reply_to(message, random.choice(ebiotList))






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
                " кс ",
                "контру",
                "cs.",
                " кс.",
                "контру.",
                "cs,",
                " кс,",
                "контру,",
                "cs?",
                " кс?",
                "контру?",
                "катаем?",
                "катаем",
                "катку?"
                ]

csListAnswers = ["Кс для пидоров.",
                 "С нубами не катаю.",
                 "А может в танки?",
                 "Нормальные пацаны в геншин играют..."]

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




