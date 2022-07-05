from flask import Flask, Blueprint
import routing, requests
from api import app2

app = Flask(__name__)
routing.iniApp(app)

@app.route('/')
def index():
    return 'index test'

@app.route('/ww888Test')
def ww888Test():
    # url = "https://requestcatcher.com/test"
    url = "https://ww888.requestcatcher.com/123"
    data = "a=1&b=2"
    header = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44"}
    result = requests.get(url = url,headers=header,data=data)
    # result = requests.get(url = url,headers=header,verify=False,data=data)
    if result.status_code == 200:
        return result.text
    else:
        response = "status_code =" + str(result.status_code)
        return response

app.register_blueprint(app2,url_prefix='/<int:pages>')

if __name__ == "__main__":
    app.run()