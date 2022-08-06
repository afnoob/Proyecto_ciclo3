from http.client import BAD_REQUEST
from flask import Flask, render_template, redirect, request, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os, sqlite3

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(24)

currentLocation = os.path.dirname(os.path.abspath(__file__))

def __init__(self):
    con=sqlite3.connect('rose.db')
    c = con.cursor
    con.commit()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        correo = request.form["username"]
        contraseña = request.form["Contraseña"]
        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query1 = "SELECT Contraseña FROM User WHERE Correo='{c}'".format(c=correo)
        cursor.execute(query1)
        data = cursor.fetchone()
        for x in data:
            separador = ""
            cadena = separador.join(str(parte) for parte in x)
        check_hash = check_password_hash(cadena, contraseña)
        if check_hash:
            session['user'] = correo
            query2 = "SELECT * FROM User WHERE Correo='{c}'".format(c=correo)
            cursor.execute(query2)
            data = cursor.fetchall()
            return render_template('inicio.html', users=data)
        else:
            flash("!Usuario o contraseña incorrecta")
            return redirect('/')
    else:
        return BAD_REQUEST

@app.route('/log-out')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/registro')
def register():
    return render_template('Registrarse.html')

@app.route('/formulario-registro', methods=['POST', 'GET'])
def registrar_informacion():
    if request.method == "POST":
        username = request.form['username']
        apellido = request.form['Apellido']
        cedula = request.form['Cedula']
        edad = request.form['Edad']
        ciudad = request.form['Ciudad']
        telefono = request.form['Telefono']
        correo = request.form['Correo']
        contraseña = generate_password_hash(request.form['Contraseña'], method="sha256")
        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT Correo FROM User WHERE Correo='{co}'".format(co=correo)
        cursor.execute(query2)
        data = cursor.fetchall()
        str_data = ''.join(map(str, data))
        electro = "('{a}',)".format(a=correo)
        if(str_data != electro):
            query1 = "INSERT INTO User VALUES ({f},'{n}','{a}',{c},{e},'{ci}',{t},'{co}','{con}','{per}')".format(f='null',n=username, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, co=correo, con=contraseña, per='user')        
            cursor.execute(query1)
            sqlconnection.commit()
            return redirect('/')
        else:
            flash("!Ya existe una cuenta registrada con ese correo")
            return redirect('/registro')

@app.route('/inicio')
def iniciar():
    if 'user' in session:
        return render_template('inicio.html', users=data)
    else:
        return "No tiene permisos para acceder a la página"
    

@app.route('/usuarios', methods=['POST', 'GET'])
def usuarios():
    if 'user' in session:
        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT * FROM User WHERE Permiso='user'"
        cursor.execute(query2)
        data = cursor.fetchall()
        return render_template('usuarios.html', users=data)
    else:
        return "No tiene permisos para acceder a la página"


@app.route('/administradores', methods=['POST', 'GET'])
def administradores():
    if 'user' in session:
        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT * FROM User WHERE Permiso='admin'"
        cursor.execute(query2)
        data = cursor.fetchall()
        return render_template('administradores.html', users=data)
    else:
        return "No tiene permisos para acceder a la página"

@app.route('/habitaciones', methods=['POST', 'GET'])
def habitaciones():
    if 'user' in session:
        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT * FROM Room"
        cursor.execute(query2)
        data = cursor.fetchall()
        return render_template('habitaciones.html', rooms=data)
    else:
        return "No tiene permisos para acceder a la página"

@app.route('/edit/<id>')
def obtener_habitacion(id):
    sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "SELECT * FROM Room WHERE id = {0}".format(id)
    cursor.execute(query2)
    data = cursor.fetchall()
    sqlconnection.commit()
    return render_template('editar_habitacion.html', edit_room = data)

@app.route('/edit-user/<id>')
def obtener_usuario(id):
    sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "SELECT * FROM User WHERE id = {0}".format(id)
    cursor.execute(query2)
    data = cursor.fetchall()
    sqlconnection.commit()
    return render_template('editar_usuario.html', edit_user = data)

@app.route('/edit-admin/<id>')
def obtener_admin(id):
    sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "SELECT * FROM User WHERE id = {0}".format(id)
    cursor.execute(query2)
    data = cursor.fetchall()
    sqlconnection.commit()
    return render_template('editar_administrador.html', edit_user = data)

@app.route('/update/<id>', methods=["POST"])
def actualizar_habitacion(id):
    if request.method == "POST":
        numero = request.form['numero']
        descripcion = request.form['descripcion']
        disponibilidad = request.form['disponibilidad']
        precio = request.form['precio']
        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "UPDATE Room SET Numero = {n}, Descripcion = '{des}', Disponibilidad = '{dis}', Precio = {p} WHERE id = {i}".format(n=numero, des=descripcion, dis=disponibilidad, p=precio, i=id)
        cursor.execute(query2)
        sqlconnection.commit()
        return redirect('/habitaciones')

@app.route('/update-user/<id>', methods=["POST"])
def actualizar_usuario(id):
    if request.method == "POST":
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        edad = request.form['edad']
        ciudad = request.form['ciudad']
        telefono = request.form['telefono']
        permisos = request.form['permisos']
        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "UPDATE User SET Nombre = '{n}', Apellido = '{a}', Cedula = {c}, Edad = {e}, Ciudad = '{ci}', Telefono ={t}, Permiso='{per}' WHERE id = {i}".format(n=nombre, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, per=permisos, i=id)
        cursor.execute(query2)
        sqlconnection.commit()
        return redirect('/usuarios')

@app.route('/update-admin/<id>', methods=["POST"])
def actualizar_admin(id):
    if request.method == "POST":
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        edad = request.form['edad']
        ciudad = request.form['ciudad']
        telefono = request.form['telefono']
        permisos = request.form['permisos']
        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "UPDATE User SET Nombre = '{n}', Apellido = '{a}', Cedula = {c}, Edad = {e}, Ciudad = '{ci}', Telefono ={t}, Permiso='{per}' WHERE id = {i}".format(n=nombre, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, per=permisos, i=id)
        cursor.execute(query2)
        sqlconnection.commit()
        return redirect('/administradores')

@app.route('/delete/<string:id>')
def eliminar_habitaciones(id):
    sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "DELETE FROM Room WHERE id = {0}".format(id)
    cursor.execute(query2)
    sqlconnection.commit()
    return redirect('/habitaciones')

@app.route('/delete-user/<string:id>')
def eliminar_usuarios(id):
    sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "DELETE FROM User WHERE id = {0}".format(id)
    cursor.execute(query2)
    sqlconnection.commit()
    return redirect('/usuarios')

@app.route('/delete-admin/<string:id>')
def eliminar_admin(id):
    sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "DELETE FROM User WHERE id = {0}".format(id)
    cursor.execute(query2)
    sqlconnection.commit()
    return redirect('/administradores')

@app.route('/añadir-usuario', methods=["POST", "GET"])
def añadir_usuario():
    if request.method == "POST":
        username = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        edad = request.form['edad']
        ciudad = request.form['ciudad']
        telefono = request.form['telefono']
        correo = request.form['correo']
        contraseña = generate_password_hash(request.form['contraseña'], method="sha256")

        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT Correo FROM User WHERE Correo='{co}'".format(co=correo)
        cursor.execute(query2)
        data = cursor.fetchall()
        str_data = ''.join(map(str, data))
        electro = "('{a}',)".format(a=correo)
        if(str_data != electro):
            query1 = "INSERT INTO User VALUES ({f},'{n}','{a}',{c},{e},'{ci}',{t},'{co}','{con}','{per}')".format(f='null',n=username, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, co=correo, con=contraseña, per='user')       
            cursor.execute(query1)
            sqlconnection.commit()
            return redirect('/usuarios')
        else:
            return "Ya existe un usuario registrado con ese correo electrónico"

@app.route('/añadir-administrador', methods=["POST", "GET"])
def añadir_administrador():
    if request.method == "POST":
        username = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        edad = request.form['edad']
        ciudad = request.form['ciudad']
        telefono = request.form['telefono']
        correo = request.form['correo']
        contraseña = generate_password_hash(request.form['contraseña'], method="sha256")

        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT Correo FROM User WHERE Correo='{co}'".format(co=correo)
        cursor.execute(query2)
        data = cursor.fetchall()
        str_data = ''.join(map(str, data))
        electro = "('{a}',)".format(a=correo)
        if(str_data != electro):
            query1 = "INSERT INTO User VALUES ({f},'{n}','{a}',{c},{e},'{ci}',{t},'{co}','{con}','{per}')".format(f='null',n=username, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, co=correo, con=contraseña, per='admin')       
            cursor.execute(query1)
            sqlconnection.commit()
            return redirect('/administradores')
        else:
            return "Ya existe un administrador registrado con ese correo electrónico"

@app.route('/añadir-habitacion', methods=["POST", "GET"])
def añadir_habitacion():
    if request.method == "POST":
        numero = request.form['numero']
        descripcion = request.form['descripcion']
        disponibilidad = request.form['disponibilidad']
        precio = request.form['precio']

        sqlconnection = sqlite3.Connection(currentLocation + "\Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT Numero FROM Room WHERE Numero='{n}'".format(n=numero)
        cursor.execute(query2)
        data = cursor.fetchall()
        str_data = ''.join(map(str, data))
        print(str_data)
        electro = "({a},)".format(a=numero)
        print(electro)
        if(str_data != electro):
            query1 = "INSERT INTO Room VALUES ({f},{n},'{d}','{dis}',{p})".format(f='null',n=numero, d=descripcion, dis=disponibilidad, p=precio)        
            cursor.execute(query1)
            sqlconnection.commit()
            return redirect('/habitaciones')
        else:
            return "Ya existe una habitacion registrado con ese número"

@app.route('/perfil')
def perfil():
    if 'user' in session:
        return render_template('Mi_perfil.html')
    else:
        return "No tiene permisos para acceder a la página"

@app.route('/lista-habitaciones')
def lista():
    if 'user' in session:
        return render_template('lista_habitaciones.html')
    else:
        return "No tiene permisos para acceder a la página"
    

@app.route('/lista-habitaciones/reserva')
def reserva():
    if 'user' in session:
        return render_template('reserva.html')
    else:
        return "No tiene permisos para acceder a la página"

@app.route('/lista-habitaciones/calificacion')
def calificacion():
    if 'user' in session:
        return render_template('estrellas.html')
    else:
        return "No tiene permisos para acceder a la página"

@app.route('/mis-reservas')
def reservar():
    if 'user' in session:
        return render_template('Mi_reserva.html')
    else:
        return "No tiene permisos para acceder a la página"


if __name__ == "__main__":
    app.run()
