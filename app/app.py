from flask import Flask
from flask_cors import CORS
from config import config

# Rutas blueprints
from routes import Producto

app=Flask(__name__)

def page_not_found(error):
    return "<h1>Not found page</h1>", 404


if __name__ == '__main__':
    
    CORS(app, resources={"*": {"origins": "http://localhost:3000"}}) #En caso de que se quiera trabajar con React
    
    # Blueprints
    app.register_blueprint(Producto.main, url_prefix='/api')
    
    app.config.from_object(config['development'])
    app.run()
    
