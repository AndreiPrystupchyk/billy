import requests, json, config
import cache
from bs4 import BeautifulSoup
from functools import reduce
from time import sleep


def steamWhoFromSpermobakiOnlineRequest(bot,messageChatId):
    listOfPlayersID = reduce((lambda x, y: x+y) , list(member["steamId"] for member in cache.steamList))
    answer = ''
    for i in range(len(listOfPlayersID)):
        sleep(0.1)
        pageRequest = requests.get(f"https://steamcommunity.com/miniprofile/{int(listOfPlayersID[i]) - 76561197960265728}")
        if pageRequest.status_code != 200:
            print(f"status code {pageRequest.status_code} returned whilst trying to fetch the enhanced rich presence info for steam user ID {i}, ignoring function")

        soup = BeautifulSoup(pageRequest.content, "html.parser")
        isPersonaInGame = soup.find_all("span", {"class": "persona in-game"})
        isPersonaOnline = soup.find_all("span", {"class": "persona online"})
        playerName = ''
        miniGameName = ''
        gameRichPresence = ''
        rich_presence = ''

        if isPersonaInGame:
            playerName = soup.find("span", class_="persona in-game").contents[0]
            miniGameName = soup.find("span", class_="miniprofile_game_name").contents[0]
            rich_presence = soup.find("span", class_="rich_presence")
            if miniGameName == 'Counter-Strike: Global Offensive':
                miniGameName = 'CS:GO'
            if rich_presence != None:
                gameRichPresence = soup.find("span", class_="rich_presence").contents[0]
            answer += f'\n*{playerName}*: {miniGameName} {gameRichPresence}'


        if isPersonaOnline:
            playerName = soup.find("span", class_="persona online").contents[0]
            answer += f'\n*{playerName}*: online'
    if answer == '':
        answer = 'Все спермачи offline :('
    bot.send_message(messageChatId, answer,parse_mode="Markdown")