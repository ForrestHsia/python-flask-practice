import youtubeFilmDataFetch
import cpbl_player_crawler
from handler import PlayerInfoHandler
import config.config as config

import models.db as db

configuration = config.config_ini()
con, cursor, client = db.db_init(configuration)

youtubeFilmDataFetch.youtubeFilmDataFetch()
# allPlayers = cpbl_player_crawler.getAllCpblPlayer()
activePlayers = cpbl_player_crawler.getActiveCpblPlayer()
hrUrl = "https://www.cpbl.com.tw/team/hr"

tmp = []
for teams in activePlayers:
    for player in teams["players"]:
        tmp.append(player)
playerLists = [f"{hrUrl}?Acnt={player['acnt']}" for player in tmp]
print("球員 url :", playerLists[0:10], f"... 限制10筆, 總共{len(playerLists)}筆")

playerinfos = PlayerInfoHandler.PlayerInfoHandler(playerLists)
playerinfos.active_players = activePlayers
playerinfos.getInfo()
playerinfos.hrLogsInsert(client)
