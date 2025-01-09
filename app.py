from flask import Flask, render_template, request, jsonify
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

#Crear la tabla si no existe
with app.app_context():
    db.create_all()

#Ordenar los registros por fecha y hora 
def ordenar_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.timestamp, reverse=True)

#Definir una ruta para la pagina principal
@app.route('/')
def index():
    #Crear un registro en la tabla log
    registros = Log.query.all()
    registros_ordenados = ordenar_por_fecha_y_hora(registros)
    return render_template('index.html',registros=registros_ordenados)

mensajes_log = []

#Funcion para agregar mensajes a la base de datos
def agregar_mensaje_log(texto):
    mensajes_log.append(texto)

    #Crear un registro en la tabla log
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()

#Token para la verificación
TOKEN_FERNANDO = 'Fernando'

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        challenge = verificar_token(request)
        return challenge
    elif request.method == 'POST':
        reponse = recibir_mensaje(request)
        return reponse

def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if token == TOKEN_FERNANDO:
        return challenge
    else:
        return jsonify({'error':'Error en la verificación del token'}),401

def recibir_mensaje(req):
    try:
        req = request.get_json()
        entry = req['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        obj_mensaje = value['message']
        agregar_mensaje_log(obj_mensaje)


        return jsonify({'message': 'EVENT_RECEIVED'})
    except Exception as e:
        return jsonify({'message': 'EVENT_RECEIVED'})

#Ejecutar la aplicacion
if __name__ == '__main__':
    #Habilitar el modo debug
    app.run(host='0.0.0.0', port=80, debug=True)

