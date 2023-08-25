import pymysql as pm
import pymongo


# DB init & con
def db_init(config):
    con = pm.connect(
        host=config["mysqlConnect"]["dbHost"],
        user=config["mysqlConnect"]["user"],
        password=config["mysqlConnect"]["pw"],
    )
    cursor = con.cursor()

    mongoCon = config["mongoConnect"]["url"] + ":" + config["mongoConnect"]["port"]
    client = pymongo.MongoClient(mongoCon)
    return con, cursor, client


def getTableList(cursor, table_title):
    """MySQL: 獲取 YT影片清單"""
    cursor.execute(
        "SELECT id,title FROM cpbl_youtube_data.cpbl_youtube_playlist where hr_record='y';"
    )
    mysql_result = cursor.fetchall()
    table_title = []
    for i in mysql_result:
        tmp = {}
        tmp["id"] = i[0]
        tmp["title"] = i[1]
        table_title.append(tmp)

    return table_title


def getAllPlayerId(cursor):
    """MySQL: 獲取 CPBL球員清單"""
    cursor.execute("SELECT Acnt,Name FROM cpbl_players.players;")
    mysql_result = cursor.fetchall()
    players = []
    for i in mysql_result:
        tmp = {}
        tmp["Acnt"] = i[0]
        tmp["Name"] = i[1]
        players.append(tmp)

    return players


def getSinglePlayerId(cursor, **kwargs):
    """MySQL: 獲取 單一CPBL球員"""
    if kwargs == None:
        return ""
    else:
        query = ""
        for k, v in kwargs.items():
            query = f"SELECT Acnt,Name FROM cpbl_players.players WHERE {k} like '{v}';"

        cursor.execute(query)
        mysql_result = cursor.fetchall()
        players = []
        for i in mysql_result:
            tmp = {}
            tmp["Acnt"] = i[0]
            tmp["Name"] = i[1]
            players.append(tmp)

        return players


def getPlayerHRlog(client, dbName, colNname, filter):
    docs = list(client[dbName][colNname].find(filter))
    return docs


print("db import finish")
