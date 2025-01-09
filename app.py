from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Crear una instancia de la aplicacion Flask
app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Crear una tabla log
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.TEXT)

#TODO: Crear la tabla si no existe
with app.app_context():
    db.create_all()

    #TODO: Ejemplos
    prueb1 = Log(texto='Prueba 1')
    prueb2 = Log(texto='Prueba 2')

    db.session.add(prueb1)
    db.session.add(prueb2)
    db.session.commit()

#TODO: Ordenar los registros por fecha y hora 
def ordenar_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.timestamp, reverse=True)

#TODO: Definir una ruta para la pagina principal
@app.route('/')
def index():
    #TODO: Crear un registro en la tabla log
    registros = Log.query.all()
    registros_ordenados = ordenar_por_fecha_y_hora(registros)
    return render_template('index.html',registros=registros_ordenados)

mensajes_log = []

#TODO: Funcion para agregar mensajes a la base de datos
def agregar_mensaje_log(texto):
    mensajes_log.append(texto)

    #TODO: Crear un registro en la tabla log
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()



#TODO: Ejecutar la aplicacion
if __name__ == '__main__':
    #TODO: Habilitar el modo debug
    app.run(host='0.0.0.0', port=80, debug=True)

