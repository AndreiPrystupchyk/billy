import openai
import config
import cache
from collections import deque

openai.api_key = config.openaitoken

bioUsers = cache.oaiBioUsers
botHistory = deque()
usersHistory = deque()

def removeBilly(message):
  if message.text.lower().startswith('/n'):
    return message.text.lower().replace('/n', '')
  elif message.text.lower().startswith('/n@spermobakibot'):
     return message.text.lower().replace('/n@spermobakibot', '')
  elif message.text.lower().startswith('/i@spermobakibot'):
     return message.text.lower().replace('/i@spermobakibot', '')
  elif message.text.lower().startswith('/i'):
    return message.text.lower().replace('/i', '')
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

def oaiMessageGetter(bot,message,bool):
    fromWho = [item for item in cache.telegramList if item.get('tgId') == message.from_user.id][0]['name']
    system_content = f'{cache.oaiBotRole} Ты сидишь в чате с {bioUsers}. Сейчас будешь отвечать на сообщение от {fromWho}.'
    if bool:
      msg = removeBilly(message)
      messages = []
      messages.append({"role": "system", "content": system_content})
      messages.append({"role": "user", "content": msg})
      usersHistory.append(msg)
      try:
          response = openai.ChatCompletion.create(
                                      model="gpt-3.5-turbo",
                                      messages=messages,
                                      max_tokens=1000,
                                      temperature=0.85)
          bot.reply_to(message, response['choices'][0]['message']['content'])
          botHistory.append(response['choices'][0]['message']['content'])
      except:
          bot.send_message(message.chat.id, 'error')
    else:
      messages = []
      messages.append({"role": "system", "content": system_content})
      usersHistory.append(message.text.lower())
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
      except:
          bot.send_message(message.chat.id, 'error')



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
