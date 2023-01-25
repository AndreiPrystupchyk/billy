import cache
import random

pidoraOtvietList = ["нет","net","нет.","net."]
daList = ["da","да"]
csListTriger = ["cs","кс","контру"]
csListAnswers = ["Кс для пидоров.",
                 "С нубами не катаю.",
                 "А может в танки?",
                 "Нормальные пацаны в генши играют..."]

def pidoraOtviet(bot, message, timeStamp):
        bot.reply_to(message, random.choice(netAnsers))
        cache.lastBotMessageTime = timeStamp

def daOtvet(bot, message, timeStamp):
    bot.reply_to(message, "Хуй на.🤣")
    cache.lastBotMessageTime = timeStamp

def csOtvet(bot, message, timeStamp):
    bot.reply_to(message, random.choice(csListAnswers))
    cache.lastBotMessageTime = timeStamp

netAnsers = [
    'Пидора ответ.🤣',
    'Хуй в пакет.',
    'Забайчен',
    'Wasted.',
    'Жизнь тебя ничему не учит...',
    'Есть пробитие.'
]