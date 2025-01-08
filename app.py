from flask import Flask, render_template

#TODO: Crear una instancia de la applicacion Flask
app = Flask(__name__)

#TODO: Definir una ruta para la pagina principal
@app.route('/')
def hola_mundo():
    return render_template('holaflask.html')

#TODO: Ejecutar la aplicacion
if __name__ == '__main__':
    #TODO: Habilitar el modo debug
    app.run(host='0.0.0.0', port=80, debug=True)
