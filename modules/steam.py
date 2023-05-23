import requests, json, config
import cache
from datetime import datetime

def steamRequest(bot,message,wholeList):
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={config.steamApiKey}&format=json&steamids={list(item["steamId"] for item in cache.spermachiList)}'
    response = json.loads(requests.get(url).text)
    answer = ''
    onlineList = []
    offlineList = []
    for i in range(len(response['response']['players'])):
        if response["response"]["players"][i]["personastate"] == 0:
            offlineList.append(f'{response["response"]["players"][i]["personaname"]}: Offline')
            #({datetime.strptime(now.strftime("%H:%M:%S"),"%H:%M:%S") - datetime.strptime(response["response"]["players"][i].get("lastlogoff").strftime("%H:%M:%S"),"%H:%M:%S")} тому назад был в стиме)
        else:
            onlineList.append(f'{response["response"]["players"][i]["personaname"]}: {response["response"]["players"][i].get("gameextrainfo","Online")}')
    for i in range(len(onlineList)):
        if i == 0:
            answer += f'{onlineList[i]}'
        else:
            answer += f'\n{onlineList[i]}'
    if wholeList:
        answer += f'\n\n'
        for i in range(len(offlineList)):
            if i == 0:
                answer += f'{offlineList[i]}'
            else:
                answer += f'\n{offlineList[i]}'
            
    bot.send_message(message.chat.id,answer)
