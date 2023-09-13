import openai
import config
import cache
from collections import deque
from datetime import datetime
import random

openai.api_key = config.openaitoken

bioUsers = cache.oaiBioUsers
botHistory = deque()
usersHistory = deque()

def removeBilly(message):
  if message.text.lower().startswith('/n'):
    return message.text.lower().replace('/n', '')
  elif message.text.lower().startswith('/n@spermobakibot'):
     return message.text.lower().replace('/n@spermobakibot', '')
  elif message.text.lower().startswith('/gpt4@spermobakibot'):
     return message.text.lower().replace('/gpt4@spermobakibot', '')
  elif message.text.lower().startswith('/gpt4'):
    return message.text.lower().replace('/gpt4', '')
  else:
     return message.text.lower()
  
def dequeLenOperator(delAllBool):
  if delAllBool:
    while botHistory:
      value = botHistory.popleft()
    while usersHistory:
      value = usersHistory.popleft()
  else:
    if len(botHistory) > cache.historyLimit:
      botHistory.popleft()
    if len(usersHistory) > cache.historyLimit:
      usersHistory.popleft()
  return

def oaiMessageGetter(bot,message,isNeedWithoutHistory):
    if message.chat.id != cache.spermobakichatid and message.chat.id != cache.andreichatid and message.chat.id != -1001816920514:
      bot.send_message(message.chat.id, 'Не могу тебе отвечать ;(')
      return
    fromWho = [item for item in cache.telegramList if item.get('tgId') == message.from_user.id][0]['name']
    todaysDate = datetime.today().strftime('%Y-%m-%d')
    timeRightNow = datetime.today().strftime('%H:%M:%S')
    system_content = f'{random.choice(cache.oaiBotRole)} Сейчас {todaysDate} дата, и время {timeRightNow}. Ты сидишь в чате с {bioUsers}. Сейчас будешь отвечать на сообщение от {fromWho}.'
    if isNeedWithoutHistory:
      msg = removeBilly(message)
      messages = []
      messages.append({"role": "system", "content": system_content})
      messages.append({"role": "user", "content": msg})
      usersHistory.append(f'{fromWho}: {msg}')
      try:
          response = openai.ChatCompletion.create(
                                      model="gpt-3.5-turbo",
                                      messages=messages,
                                      max_tokens=1000,
                                      temperature=0.85)
          bot.reply_to(message, response['choices'][0]['message']['content'])
          botHistory.append(response['choices'][0]['message']['content'])
      except Exception as e:
        bot.send_message(message.chat.id, str(e))
    else:
      messages = []
      messages.append({"role": "system", "content": system_content})
      usersHistory.append(f'{fromWho}: {message.text.lower()}')
      for i in range(len(usersHistory)):
        messages.append({'role':'user', 'content':usersHistory[i]})
        if i < len(botHistory):
          messages.append({'role':'assistant', 'content':botHistory[i]})
      try:
        response = openai.ChatCompletion.create(
                                      model="gpt-3.5-turbo",
                                      messages=messages,
                                      max_tokens=1000,
                                      temperature=0.85)
        bot.reply_to(message, response['choices'][0]['message']['content'])
        botHistory.append(response['choices'][0]['message']['content'])
        dequeLenOperator(False)
      except Exception as e:
        bot.send_message(message.chat.id, str(e))

def pdCongrats(bot,message):
    todaysDate = datetime.today().strftime('%Y-%m-%d')
    timeRightNow = datetime.today().strftime('%H:%M:%S')
    name = [item for item in cache.telegramList if item.get('tgId') == cache.pidorOfDay['id']]
    system_content = f'{cache.oaiBotRole}. Сейчас {todaysDate} дата, и время {timeRightNow}. Ты сидишь в чате c {bioUsers}. Твой гейрадар показал, что {name[0]["name"]} сегодня пидарас дня, поздравь его с этим.'
    messages = []
    messages.append({"role": "system", "content": system_content})
    try:
        response = openai.ChatCompletion.create(
                                      model="gpt-3.5-turbo",
                                      messages=messages,
                                      max_tokens=1000,
                                      temperature=0.90)
        bot.send_message(message.chat.id, response['choices'][0]['message']['content'])
        botHistory.append(response['choices'][0]['message']['content'])
    except Exception as e:
      bot.send_message(message.chat.id, str(e))


def gpt4(bot, message):
  if message.chat.id != cache.spermobakichatid and message.chat.id != cache.andreichatid and message.chat.id != -1001816920514:
    bot.send_message(message.chat.id, 'Не могу тебе отвечать ;(')
    return
  fromWho = [item for item in cache.telegramList if item.get('tgId') == message.from_user.id][0]['name']
  todaysDate = datetime.today().strftime('%Y-%m-%d')
  timeRightNow = datetime.today().strftime('%H:%M:%S')
  system_content = f'Сейчас {todaysDate} дата, и время {timeRightNow}. Сейчас будешь отвечать на сообщение от {fromWho}.'
  msg = removeBilly(message)
  messages = []
  messages.append({"role": "system", "content": system_content})
  messages.append({"role": "user", "content": msg})
  try:
    response = openai.ChatCompletion.create(
                                      model="gpt-4",
                                      messages=messages,
                                      max_tokens=1000,
                                      temperature=0.8)
    bot.reply_to(message, response['choices'][0]['message']['content'])
    botHistory.append(response['choices'][0]['message']['content'])
  except Exception as e:
    bot.send_message(message.chat.id, str(e))




def oaiImageGenerator(bot,message):
  request = removeBilly(message)
  if request == '':
     bot.send_message(message.chat.id, 'Дай запрос, пупсик :*')
  try:
    text = message.text
    response = openai.Image.create(
    prompt=text,
    n=1,
    size="512x512"
  )
    image_url = response['data'][0]['url']
    bot.send_message(message.chat.id, image_url)
  
  except:
    bot.send_message(message.chat.id, 'error')
