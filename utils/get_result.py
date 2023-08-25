"""取"""

import json
import traceback
import requests as req
from utils import general_function as gf


#
def get_playlist_result(url):
    """取 YT 頻道內的影片清單"""
    container = []
    bad_url_container = []
    result = req.get(url, timeout=10).json()
    totalResults = result["pageInfo"]["totalResults"]
    resultsPerPage = result["pageInfo"]["resultsPerPage"]
    container.append(result)
    for i in range(0, totalResults // resultsPerPage):
        try:
            if result.get("nextPageToken") is not None:
                url = url + f"&pageToken={result['nextPageToken']}"
                result = req.get(url, timeout=10).json()
            else:
                result = req.get(url, timeout=10).json()
        except Exception as e:
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            errMsg = 'File "{}", line {}, in {}: [{}] {}'.format(
                fileName, lineNum, funcName, error_class, detail
            )

            bad_result = {}
            bad_result["url"] = url
            bad_result["error"] = errMsg
            bad_url_container.append(bad_result)
        container.append(result)
    # with open("./data/playlist_result.json", "w+", encoding="utf8") as r:
    #     json.dump(container, r)
    if len(bad_url_container) > 0:
        with open("./data/bad/bad_playlist_url.json", "w+", encoding="utf8") as r:
            json.dump(bad_url_container, r)

    return container


#
def get_playlistItems_result(id_value, url, eng_title):
    """取 YT API response 的page token 跳頁用"""
    container = []
    bad_url_container = []
    result = req.get(url, timeout=10).json()
    totalResults = result["pageInfo"]["totalResults"]
    resultsPerPage = result["pageInfo"]["resultsPerPage"]

    tmp = {}
    tmp["playList"] = id_value
    tmp["result"] = []

    tmp["result"].append(result)

    for i in range(0, totalResults // resultsPerPage):
        try:
            if result.get("nextPageToken") is not None:
                url = url + f"&pageToken={result['nextPageToken']}"
                result = req.get(url, timeout=10).json()
            elif totalResults == 50:
                break
            else:
                result = req.get(url, timeout=10).json()

        except Exception as e:
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            errMsg = 'File "{}", line {}, in {}: [{}] {}'.format(
                fileName, lineNum, funcName, error_class, detail
            )

            bad_result = {}
            bad_result["url"] = url
            bad_result["error"] = errMsg
            bad_url_container.append(bad_result)

        tmp["result"].append(result)
    # tmp["bad_result"] = bad_url_container
    if len(bad_url_container) > 0:
        with open(
            f"./data/bad/bad_playlist_item_url_{eng_title}.json",
            "w+",
            encoding="utf8",
        ) as r:
            json.dump(bad_url_container, r)
    container.append(tmp)
    return container
