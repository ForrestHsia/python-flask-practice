import concurrent.futures
import re
import time
import requests
import browser_cookie3
from bs4 import BeautifulSoup
import const

const.positionNum = {
    "投手": "1",
    "捕手": "2",
    "一壘手": "",
    "二壘手": "",
    "三壘手": "",
    "游擊手": "",
    "右外野手": "7",
    "中外野手": "8",
    "左外野手": "9",
}


def apiCategory(url):
    role = re.compile(r"(\w+)[\?]")
    result = role.search(url)
    category = result.group()
    return category[:-1]


def idToTitle(id, table_title):
    for table in table_title:
        if id == table["id"]:
            return table["eng_title"]
    return "bad_table"


def title_correction(string):
    role = re.compile(r"\'")
    result = role.sub("", string)
    return result


def getTime(int):
    """取時間 1 : yyyymmdd, 2 : yyyymmddhhmm, 3 : unixtime"""
    time_now = time.localtime()
    match int:
        case 1:
            time_stamp = (
                str(time_now.tm_year)
                + str(time_now.tm_mon).zfill(2)
                + str(time_now.tm_mday).zfill(2)
            )
            return time_stamp
        case 2:
            time_stamp = (
                str(time_now.tm_year)
                + str(time_now.tm_mon).zfill(2)
                + str(time_now.tm_mday).zfill(2)
                + str(time_now.tm_hour).zfill(2)
                + str(time_now.tm_min).zfill(2)
            )
            return time_stamp
        case 3:
            return time.time()
        case _:
            return time.time()


def GetCpblCookies():
    default = requests.get("https://www.cpbl.com.tw/", verify=False, timeout=10)
    cookies = default.cookies.get_dict()
    cookie = ""
    for i, j in cookies.items():
        cookie += i + "=" + j + ";"
    return {"cookies": cookies, "cookieString": cookie[:-1]}


def tryExcept(query, cursor, bad_result_outside):
    try:
        cursor.execute(query)
    except Exception as e:
        error_class = e.__class__.__name__  # 取得錯誤類型
        detail = e.args[0]  # 取得詳細內容
        if detail != 1062:
            print("Failed Query:", query)
            bad_result = {}
            bad_result["query"] = query
            bad_result["error"] = error_class
            bad_result["detail"] = str(e)
            bad_result_outside.append(bad_result)


# def positionToNum(string):

# def activePlayerParse()
