from flask import Blueprint

app2 = Blueprint('app2', __name__,static_folder='static')

# @app2.route('/<int:page>/app2')
# def show(page):
#     return "Hello Blueprint app2 at {page}"

@app2.route('/app2')
def show(pages):
    return f"Hello Blueprint app2 at {pages}"