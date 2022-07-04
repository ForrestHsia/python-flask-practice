from pymysql import NULL


def init_app(app):
    @app.route("/data/<name>",methods =['GET'] )
    def getString(name):
        print(f"type of name: {type(name)}")
        return 'String -> {}'.format(name)
    
    @app.route("/data/",methods =['GET'] )
    def getEmptyString():
        return 'Input is Null or Empty'