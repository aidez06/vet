from flask import Flask
from client.routes.auth_routes import auth 
from client.routes.public_routes import public 


app = Flask(__name__)

app.register_blueprint(public, url_prefix='/public') 
app.register_blueprint(auth, url_prefix='/auth')
print(app.blueprints)  # Should show both 'auth' and 'public'

if __name__ == '__main__':
    app.run(debug=True)