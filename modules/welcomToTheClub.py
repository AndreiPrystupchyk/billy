import cache

pidorList = ["пидар","пидор","пидр","pidar","pidor"]

def welcomToTheClub(bot,message,timeStamp):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id != bot.user.id:
            bot.send_message(message.chat.id, "Welcome to the club buddy!",reply_to_message_id=message.reply_to_message.message_id)
            cache.lastBotMessageTime = timeStamp
    else:
        bot.send_message(message.chat.id, "Welcome to the club buddy!")
        cache.lastBotMessageTime = timeStamp