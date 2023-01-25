import cache
import random

bottleList = ["бутылка","бутылку","🍾"]
sitAnswers = [
    "Присел бы...🍾",
    "Что-то я застоялся.🍾",
    "Уфф🍾",
    "Вижу знатока.🍾"
]

def sitOnBottle(bot,message,timeStamp):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id != bot.user.id:
            bot.send_message(message.chat.id, random.choice(sitAnswers),reply_to_message_id=message.reply_to_message.message_id)
            cache.lastBotMessageTime = timeStamp
    else:
        bot.send_message(message.chat.id, random.choice(sitAnswers))
        cache.lastBotMessageTime = timeStamp
