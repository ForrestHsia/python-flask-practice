"""fetch_result 處理返回結果，拼裝成我要形式"""


def fetch_playlist(apiCategory, result):
    """拼裝YT的 影片清單 內容"""
    container = []
    if apiCategory == "playlists":
        for i in result:
            for j in i["items"]:
                tmp2 = {}
                tmp2["id"] = j["id"]
                tmp2["title"] = j["snippet"]["title"]
                tmp2["count"] = j["contentDetails"]["itemCount"]
                container.append(tmp2)
    return container


# 取api返回的頁面結果
def fetch_playlistItems(results):
    """拼裝YT影片清單的各清單 內容"""
    container = []
    for result in results:
        tmp = {}
        tmp["playList"] = result["playList"]
        tmp["result"] = []
        for i in result["result"]:
            for j in i["items"]:
                tmp2 = {}
                tmp2["video_title"] = j["snippet"]["title"]
                tmp2["video_id"] = j["snippet"]["resourceId"]["videoId"]
                tmp2["video_date"] = j["snippet"]["publishedAt"]
                tmp["result"].append(tmp2)
        container.append(tmp)
    return container
