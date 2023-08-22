from flask import Flask
import routing, requests
from view.api import app2
from flask_pymongo import PyMongo

app = Flask(__name__)
routing.iniApp(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/tgMessage"
mg = PyMongo(app)

class PlayerHRLog:
    

@app.route("/", methods=["GET"])
def index():
    return "index test"


@app.route("/ww888Test/", methods=["POST"])
def ww888Test():
    # url = "https://requestcatcher.com/test"
    url = "https://ww888.requestcatcher.com/123"
    data = "a=1&b=2"
    header = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44"
    }
    result = requests.get(url=url, headers=header, verify=False, data=data)

    if result.status_code == 200:
        return result.text
    else:
        response = "status_code =" + str(result.status_code)
        return response


@app.route("/player/cpbl/<name>", methods=["POST"])
def getCPBLPlayerHRLogs(name):
    hrLogs = list(mg.db.get_collection("HRLogSplit").find({"player": name}))
    print(hrLogs)
    return "success"


# app.register_blueprint(app2, url_prefix="/<int:pages>")

if __name__ == "__main__":
    app.debug = True
    app.run()
