def iniApp(app):
    @app.route('/auth')
    def auths():
        return 'auth'
    
    @app.route('/data/appInfo/<name>',methods=['GET'])
    def queryDataMessageByName(name):
        print("type(name) : ", type(name))
        return 'String => {}'.format(name)

    @app.route('/data/appInfo/<int:id>',methods=['GET'])
    def queryDataMessageById(id):
        print("type(id) : ", type(id))
        return 'Int => {}'.format(id)


