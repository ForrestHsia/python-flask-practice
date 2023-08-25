"""無法以json形式取得資料時，以這個handler處理"""

import concurrent.futures
import random
import time
from urllib.parse import urlparse
import re
import requests
import config.config as config

from bs4 import BeautifulSoup as bs
from utils import general_function as gf

requests.packages.urllib3.disable_warnings()

objRoot = "[handler]"
moduleName = "[PlayerHandler]"


class PlayerInfoHandler:

    """處理球員頁面 html內容 為主"""

    def __init__(self, urls):
        # def __init__(self, urls, mongoClient):
        self.urls = urls
        self.resps = []
        self.active_players = []

    # def __getConfig(self):
    #     return self._config

    def __getAllPlayers(self, url):
        """private function, 僅內部以 單一地址 發請求用"""
        acnt = urlparse(url).query[5:]

        configs = config.config_ini()
        configs["cpbl_hr_log_header"]["referer"] += f"?acnt={acnt}"

        response = requests.get(
            url,
            timeout=15,
            verify=False,
            headers=configs["cpbl_hr_log_header"],
        )
        resp = {}
        sleepTime = 0.00

        if response.status_code == 200:
            resp["isSuccess"] = True
            resp["acnt"] = acnt
            resp["content"] = response.text
            resp["created"] = gf.getTime(1)
            resp["updated"] = gf.getTime(1)
            sleepTime = random.uniform(10, 15)
            print(f"url done, sleepTime: {sleepTime} sec")
        else:
            resp["isSuccess"] = False
            resp["url"] = url
            resp["acnt"] = acnt
            resp["statusCode"] = response.status_code
            sleepTime = random.uniform(5, 8)  # response為失敗的話，儘早開始 下個req
            print(
                f"url failed: {url}, sleepTime: {sleepTime} sec, statusCode: {response.status_code}"
            )

        time.sleep(sleepTime)
        self.resps.append(resp)

    def __getAllFailedPlayers(self, resp):
        """private function, 僅內部以 單一地址 發請求用"""
        if resp["isSuccess"] == False:
            self.__getAllPlayers(resp["url"])

    def __makePlayerInfo(self, resp):
        if resp["isSuccess"] is True:
            playerInfo = bs(resp["content"], "html.parser")
            playerBrief = playerInfo.find("div", class_="PlayerBrief").find("dl")
            hrTable = playerInfo.find("div", class_="RecordTable")

            tagsDD = playerBrief.find_all("dd")
            name = playerBrief.find("div", class_="name").getText()
            name = re.sub("\d", "", name)
            resp["name"] = name
            resp["team"] = playerBrief.find("div", class_="team").getText()

            for tag in tagsDD:
                resp[tag["class"][0]] = (
                    playerBrief.find("dd", class_=tag["class"][0])
                    .find("div", class_="desc")
                    .getText()
                )

            hrLog = []
            if resp["pos"] != "投手":
                hrLogString = ""
                for j in hrTable.find_all("th"):
                    hrLogString += j.getText() + ","
                hrLogString = hrLogString[0:-1]
                hrLog.append(hrLogString)

                for i in hrTable.find_all("tr"):
                    hrLogString = ""
                    for j in i.find_all("td"):
                        # print(j.getText())
                        hrLogString += j.getText() + ","

                    if len(hrLogString) == 0:
                        continue
                    hrLogString = hrLogString[0:-1]
                    hrLog.append(hrLogString)
            resp["hrLog"] = hrLog
            resp.pop("content")

    def getInfo(self):
        """private function, 僅內部以 單一地址 發請求用"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
            executor.map(self.__getAllPlayers, self.urls, timeout=20)
        print(objRoot, moduleName, "__getAllPlayers() execute done.")

        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
            executor.map(self.__makePlayerInfo, self.resps, timeout=0)
        print(objRoot, moduleName, "__makePlayerInfo() execute done.")

    def __hrLogsInsert(self, client, resp):
        filter = {"acnt": resp["acnt"]}

        hrlog = list(client["tgMessage"]["HRLog"].find(filter))
        if len(hrlog) == 0:
            client["tgMessage"]["HRLog"].insert_one(resp)
        elif len(hrlog[0]["hrLog"]) <= len(resp["hrLog"]):
            updatedTime = gf.getTime(1)
            updated = {
                "$set": {
                    "updated": updatedTime,
                    "hrLog": resp["hrLog"],
                    "name": resp["name"],
                    "team": resp["team"],
                    "content": None,
                }
            }
            client["tgMessage"]["HRLog"].update_one(filter, update=updated)

    def __hrLogsSplitInsert(self, client, resp):
        filter = {"acnt": resp["acnt"]}
        playerHRLength = len(resp["hrLog"]) - 1  # 這是最新的球員全壘打數
        hrLogs = list(client["tgMessage"]["HRLogSplit"].find(filter))  # 這是 更新前的全壘打數

        mongoInsert = []
        playerHR = {}
        playerHR["hrLog"] = []
        tagArray = [
            "hrNumber",
            "year",
            "game",
            "inning",
            "date",
            "stadium",
            "pitcher",
            "rbi",
            "note",
            "player",
            "acnt",
            "team",
        ]

        if resp["pos"] == "投手":
            return
        elif (playerHRLength > 0) and (len(hrLogs) == 0):  # 沒有任何split HR，走這裡
            playerHR = {}
            playerHR["hrLog"] = []
            for j, hr in enumerate(resp["hrLog"], start=0):
                if j == 0:
                    continue
                else:
                    a = hr.split(",")
                    eachHR = {}
                    for k, v in enumerate(a):
                        if k in [0, 7]:
                            eachHR[tagArray[k]] = int(v)
                        else:
                            eachHR[tagArray[k]] = v
                    eachHR[tagArray[9]] = resp["name"]
                    eachHR[tagArray[10]] = resp["acnt"]
                    playerHR["hrLog"].append(eachHR)
            playerHR[tagArray[9]] = resp["name"]
            playerHR[tagArray[10]] = resp["acnt"]
            playerHR[tagArray[11]] = resp["team"]
            mongoInsert.append(playerHR)
        elif (playerHRLength > 0) and (len(hrLogs) >= 1):  # 有split HR後，走這裡
            playerHR = {}
            playerHR["hrLog"] = []
            for j, hr in enumerate(resp["hrLog"], start=0):
                if j <= len(hrLogs):
                    continue
                else:
                    a = hr.split(",")
                    eachHR = {}
                    for k, v in enumerate(a):
                        eachHR[tagArray[k]] = v
                    eachHR[tagArray[9]] = resp["name"]
                    eachHR[tagArray[10]] = resp["acnt"]
                    playerHR["hrLog"].append(eachHR)
            playerHR[tagArray[9]] = resp["name"]
            playerHR[tagArray[10]] = resp["acnt"]
            playerHR[tagArray[11]] = resp["team"]
            mongoInsert.append(playerHR)

        if len(mongoInsert) < 1:
            print("無全壘打更新")
        elif len(mongoInsert[0]["hrLog"]) >= 1:
            print(
                "全壘打更新, ",
                mongoInsert[0]["hrLog"][0:10],
                f"限制顯示10筆, 總長:{len(mongoInsert[0]['hrLog'])}筆",
            )
            for i in mongoInsert:
                client["tgMessage"]["HRLogSplit"].insert_many(i["hrLog"])

    def hrLogsInsert(self, client):
        for resp in self.resps:
            if resp["isSuccess"] is True:
                self.__hrLogsInsert(client, resp)
                self.__hrLogsSplitInsert(client, resp)
        print(objRoot, moduleName, "hrLogsInsert() execute done.")
