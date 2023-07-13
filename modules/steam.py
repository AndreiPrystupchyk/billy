import requests, json, config
import cache

status = {0:'Offline', 1:'Online', 2:'Busy', 3:'Away', 4:'Snooze', 5:'looking to trade', 6:'looking to play'}


def steamWhoFromSpermobakiOnlineRequest(bot,messageChatId):
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={config.steamApiKey}&format=json&steamids={list(member["steamId"] for member in cache.steamList)}'
    response = json.loads(requests.get(url).text)
    answer = ''
    for i in range(len(response['response']['players'])):
        if response["response"]["players"][i]["personastate"] != 0:
            answer += f'\n{response["response"]["players"][i]["personaname"]}: {response["response"]["players"][i].get("gameextrainfo",status[response["response"]["players"][i]["personastate"]])}'
    if not answer == '':
        bot.send_message(messageChatId,answer)
    else:
        bot.send_message(messageChatId,'Все спермачи offline :(')