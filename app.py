from flask import Flask, render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/registro')
def register():
    return render_template('Registrarse.html')

@app.route('/inicio')
def iniciar():
    return render_template('inicio.html')

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/administradores')
def administradores():
    return render_template('administradores.html')

@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

if __name__ == "__main__":
    app.run()


