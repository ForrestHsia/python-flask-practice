import config.config as config
import models.db as db

from dataclasses import dataclass
from dataclasses import field
import dacite


configuration = config.config_ini()
con, cursor, client = db.db_init(configuration)


def getHRLogs(name):
    filter = {"player": name}

    hrLogs = list(client["tgMessage"]["HRLogSplit"].find(filter))

    @dataclass
    class HRLogs:
        hrNumber: int = field(init=False, default=0)
        year: str = field(init=False, default="")
        inning: str = field(init=False, default="")
        date: str = field(init=False, default="")
        pitcher: str = field(init=False, default="")
        player: str = field(init=False, default="")
        acnt: str = field(init=False, default="")
        videoUrl: str = field(init=False, default_factory=list)

        def inningConverter(self) -> int:
            inning = {
                "1": "一局",
                "2": "二局",
                "3": "三局",
                "4": "四局",
                "5": "五局",
                "6": "六局",
                "7": "七局",
                "8": "八局",
                "9": "九局",
                "10": "十局",
                "11": "十一局",
                "12": "十二局",
            }
            return inning[self.inning]

        def ytUrlMaker(self, videos) -> list:
            for video in videos:
                tmp = []
                ytFilmUrl = "https://www.youtube.com/watch?v=" + video[0]
                ytFilmDes = video[1]
                tmp.append(ytFilmUrl)
                tmp.append(ytFilmDes)
                self.videoUrl.append(tmp)

        def getYTChannelIdAndTitle(self, cursor):
            date = self.date.replace("/", "-")
            inning = self.inningConverter()
            cursor.execute(
                f"SELECT * FROM cpbl_youtube_data.cpbl_youtube_playlist where `max_time` > '{date}' and `min_time` < '{date}'and `min_time` > '2012-12-31' and hr_record = 'y' "
            )
            table = list(cursor.fetchall())
            if len(table) > 1:
                print("請檢查table的YT撥放清單時間區間, table 為:", table)
            elif len(table) == 0:
                print(f"編號:{self.hrNumber} 這一支沒有影片")
                return

            cursor.execute(
                f"SELECT * FROM cpbl_youtube_data.{table[0][2]} where video_date like '{date}%' and video_title like '%{inning}%' and video_title like '%{self.player}%'"
            )

            video = list(cursor.fetchall())
            self.ytUrlMaker(video)

    hrLogsSum = []

    for hr in hrLogs:
        hrLog = dacite.from_dict(HRLogs, hr)
        hrLog.getYTChannelIdAndTitle(cursor=cursor)
        hrLogsSum.append(hrLog)

    return hrLogsSum
