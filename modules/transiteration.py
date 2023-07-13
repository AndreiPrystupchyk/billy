import re

layoutEn = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                           'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                           "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                           'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
layoutRu = dict(zip(map(ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                           'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
                           "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                           'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'))
def getter(bot,message):
    if message.reply_to_message:
        if has_cyrillic(message.reply_to_message.text):
             bot.send_message(message.chat.id,message.reply_to_message.text.translate(layoutRu))
        else:
            bot.send_message(message.chat.id,message.reply_to_message.text.translate(layoutEn))
    else:
            bot.send_message(message.chat.id,'Нужно процитировать кого-то.')

def has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))