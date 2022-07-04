from flask import Flask
import router

app = Flask(__name__)
router.init_app(app)

@app.route('/')
def index():
    return "index test"

if __name__ == '__main__':
    app.run(debug=True)