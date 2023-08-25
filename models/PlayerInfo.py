import db
from dataclasses import dataclass
from dataclasses import field
from typing import List


class PlayerHRInfos:
    def __init__(self, acnt, player, team):
        self.__acnt = acnt
        self.__player = player
        self.__team = team
