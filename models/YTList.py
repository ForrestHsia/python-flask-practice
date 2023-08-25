from dataclasses import dataclass
from dataclasses import field
import dacite


@dataclass
class YTChannelList:
    id: str
    title: int
    eng_title: str
    hr_record: str

    def getYTChannelIdAndTitle(self, cursor, query) -> int:
        return self.id
