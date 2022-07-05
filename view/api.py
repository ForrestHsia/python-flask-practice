from flask import Blueprint

app2 = Blueprint('app2', __name__)

@app2.route('/app2')
def show(page):
    return "Hello Blueprint app2"