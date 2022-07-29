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

@app.route('/perfil')
def perfil():
    return render_template('Mi_perfil.html')

@app.route('/lista-habitaciones')
def lista():
    return render_template('lista_habitaciones.html')

@app.route('/lista-habitaciones/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/lista-habitaciones/calificacion')
def calificacion():
    return render_template('estrellas.html')

if __name__ == "__main__":
    app.run()
