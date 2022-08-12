from http.client import BAD_REQUEST
from flask import Flask, render_template, redirect, request, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os, sqlite3
from datetime import datetime 

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(24)

#currentLocation = os.path.dirname(os.path.abspath(__file__))

def __init__(self):
    con=sqlite3.connect('Rose.db')
    c = con.cursor
    con.commit()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/datos-personales')
def datos_personales():
    return render_template('datos_personales.html')

@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        correo = request.form["username"]
        contraseña = request.form["Contraseña"]
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query1 = "SELECT Contraseña FROM User WHERE Correo='{c}'".format(c=correo)
        cursor.execute(query1)
        data = cursor.fetchone()
        try:
            for x in data:
                separador = ""
                cadena = separador.join(str(parte) for parte in x)
        except:
            flash("!Usuario o contraseña incorrecta")
            return redirect('/')
        check_hash = check_password_hash(cadena, contraseña)
        if check_hash:
            session['user'] = correo
            query2 = "SELECT * FROM User WHERE Correo='{c}'".format(c=correo)
            cursor.execute(query2)
            user_data = cursor.fetchall()
            return render_template('inicio.html', users=user_data)
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
    try:
        if request.method == "POST":
            checkbox=request.form["check"]
            username = request.form['username']
            apellido = request.form['Apellido']
            cedula = request.form['Cedula']
            edad = request.form['Edad']
            ciudad = request.form['Ciudad']
            telefono = request.form['Telefono']
            correo = request.form['Correo']
            contraseña = generate_password_hash(request.form['Contraseña'], method="sha256")
            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            query2 = "SELECT Correo FROM User WHERE Correo='{co}'".format(co=correo)
            cursor.execute(query2)
            data = cursor.fetchall()
            str_data = ''.join(map(str, data))
            electro = "('{a}',)".format(a=correo)
            try:
                if(str_data != electro and checkbox=='True'):
                    query1 = "INSERT INTO User VALUES ({f},'{n}','{a}',{c},{e},'{ci}',{t},'{co}','{con}','{per}')".format(f='null',n=username, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, co=correo, con=contraseña, per='user')        
                    cursor.execute(query1)
                    sqlconnection.commit()
                    flash("!Usuario registrado con éxito")
                    return redirect('/')
            except:
                flash("!Los campos Cédula, Edad y Teléfono deben ser de caracter numérico")
                return redirect('/registro')
            else:
                flash("!Ya existe una cuenta registrada con ese correo")
                return redirect('/registro')
    except:
        flash("Por favor acepte la política de tratamiento de datos personales")
        return redirect('/registro')

@app.route('/inicio')
def iniciar():
    if 'user' in session:
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
        cursor.execute(query1)
        user_data = cursor.fetchall()
        return render_template('inicio.html', users=user_data)
    else:
        return "No tiene permisos para acceder a la página"
    

@app.route('/usuarios', methods=['POST', 'GET'])
def usuarios():
    if 'user' in session:
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT * FROM User WHERE Permiso='user'"
        cursor.execute(query2)
        data = cursor.fetchall()
        query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
        cursor.execute(query1)
        user_data = cursor.fetchall()
        return render_template('usuarios.html', users=data, user_login=user_data)
    else:
        return "No tiene permisos para acceder a la página"


@app.route('/administradores', methods=['POST', 'GET'])
def administradores():
    if 'user' in session:
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT * FROM User WHERE Permiso='admin'"
        cursor.execute(query2)
        data = cursor.fetchall()
        query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
        cursor.execute(query1)
        user_data = cursor.fetchall()
        return render_template('administradores.html', users=data, user_login=user_data)
    else:
        return "No tiene permisos para acceder a la página"

@app.route('/habitaciones', methods=['POST', 'GET'])
def habitaciones():
    if 'user' in session:
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT * FROM Room"
        cursor.execute(query2)
        data = cursor.fetchall()
        query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
        cursor.execute(query1)
        user_data = cursor.fetchall()
        return render_template('habitaciones.html', rooms=data, user_login=user_data)
    else:
        return "No tiene permisos para acceder a la página"

@app.route('/edit/<id>')
def obtener_habitacion(id):
    sqlconnection = sqlite3.Connection("Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "SELECT * FROM Room WHERE id = {0}".format(id)
    cursor.execute(query2)
    data = cursor.fetchall()
    sqlconnection.commit()
    query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
    cursor.execute(query1)
    user_data = cursor.fetchall()
    return render_template('editar_habitacion.html', edit_room = data, user_login=user_data)

@app.route('/edit-user/<id>')
def obtener_usuario(id):
    sqlconnection = sqlite3.Connection("Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "SELECT * FROM User WHERE id = {0}".format(id)
    cursor.execute(query2)
    data = cursor.fetchall()
    sqlconnection.commit()
    query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
    cursor.execute(query1)
    user_data = cursor.fetchall()
    return render_template('editar_usuario.html', edit_user = data, user_login=user_data)

@app.route('/edit-admin/<id>')
def obtener_admin(id):
    sqlconnection = sqlite3.Connection("Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "SELECT * FROM User WHERE id = {0}".format(id)
    cursor.execute(query2)
    data = cursor.fetchall()
    sqlconnection.commit()
    query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
    cursor.execute(query1)
    user_data = cursor.fetchall()
    return render_template('editar_administrador.html', edit_user = data, user_login=user_data)

@app.route('/update/<id>', methods=["POST"])
def actualizar_habitacion(id):
    try:
        if request.method == "POST":
            numero = request.form['numero']
            descripcion = request.form['descripcion']
            disponibilidad = request.form['disponibilidad']
            precio = request.form['precio']
            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            try:
                query2 = "UPDATE Room SET Numero = {n}, Descripcion = '{des}', Disponibilidad = '{dis}', Precio = {p} WHERE id = {i}".format(n=numero, des=descripcion, dis=disponibilidad, p=precio, i=id)
                cursor.execute(query2)
                sqlconnection.commit()
                flash("!Habitación actualizada con éxito")
                return redirect('/habitaciones')
            except:
                flash("¡Error! ¡Los campos Número y Precio deben ser numéricos")
                return redirect('/habitaciones')
    except:
        flash("¡Error al momento de actualizar la habitación")
        return redirect('/habitaciones')

@app.route('/update-user/<id>', methods=["POST"])
def actualizar_usuario(id):
    try:
        if request.method == "POST":
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            cedula = request.form['cedula']
            edad = request.form['edad']
            ciudad = request.form['ciudad']
            telefono = request.form['telefono']
            permisos = request.form['permisos']
            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            try:
                query2 = "UPDATE User SET Nombre = '{n}', Apellido = '{a}', Cedula = {c}, Edad = {e}, Ciudad = '{ci}', Telefono ={t}, Permiso='{per}' WHERE id = {i}".format(n=nombre, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, per=permisos, i=id)
                cursor.execute(query2)
                sqlconnection.commit()
                query3 = "UPDATE Reservas SET Cedula = '{ce}' WHERE id = {i}".format(ce=cedula,)
                cursor.execute(query3)
                sqlconnection.commit()

                flash("!Usuario editado con éxito")
                return redirect('/usuarios')
            except:
                flash("¡Error! !Los campos Cédula, Edad y Teléfono deben ser numéricos")
                return redirect('/usuarios')
    except:
        flash("¡Error al momento de actualizar el usuario")
        return redirect('/usuarios')


@app.route('/update-admin/<id>', methods=["POST"])
def actualizar_admin(id):
    try:
        if request.method == "POST":
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            cedula = request.form['cedula']
            edad = request.form['edad']
            ciudad = request.form['ciudad']
            telefono = request.form['telefono']
            permisos = request.form['permisos']
            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            try:
                query2 = "UPDATE User SET Nombre = '{n}', Apellido = '{a}', Cedula = {c}, Edad = {e}, Ciudad = '{ci}', Telefono ={t}, Permiso='{per}' WHERE id = {i}".format(n=nombre, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, per=permisos, i=id)
                cursor.execute(query2)
                sqlconnection.commit()
                flash("!Administrador editado con éxito")
                return redirect('/administradores')
            except:
                flash("¡Error! !Los campos Cédula, Edad y Teléfono deben ser numéricos")
                return redirect('/administradores')
    except:
        flash("¡Error al momento de actualizar el administrador")
        return redirect('/administradores')

@app.route('/delete/<string:id>')
def eliminar_habitaciones(id):
    sqlconnection = sqlite3.Connection("Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "DELETE FROM Room WHERE id = {0}".format(id)
    cursor.execute(query2)
    sqlconnection.commit()
    flash("¡La habitación ha sido eliminada con éxito")
    return redirect('/habitaciones')

@app.route('/delete-user/<string:id>')
def eliminar_usuarios(id):
    sqlconnection = sqlite3.Connection("Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "DELETE FROM User WHERE id = {0}".format(id)
    cursor.execute(query2)
    sqlconnection.commit()
    flash("!El usuario se ha eliminado con éxito")
    return redirect('/usuarios')

@app.route('/delete-admin/<string:id>')
def eliminar_admin(id):
    sqlconnection = sqlite3.Connection("Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "DELETE FROM User WHERE id = {0}".format(id)
    cursor.execute(query2)
    sqlconnection.commit()
    flash("!El administrador se ha eliminado con éxito")
    return redirect('/administradores')

@app.route('/añadir-usuario', methods=["POST", "GET"])
def añadir_usuario():
    try:
        if request.method == "POST":
            username = request.form['nombre']
            apellido = request.form['apellido']
            cedula = request.form['cedula']
            edad = request.form['edad']
            ciudad = request.form['ciudad']
            telefono = request.form['telefono']
            correo = request.form['correo']
            contraseña = generate_password_hash(request.form['contraseña'], method="sha256")

            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            query2 = "SELECT Correo FROM User WHERE Correo='{co}'".format(co=correo)
            cursor.execute(query2)
            data = cursor.fetchall()
            str_data = ''.join(map(str, data))
            electro = "('{a}',)".format(a=correo)
            try:
                if(str_data != electro):
                    query1 = "INSERT INTO User VALUES ({f},'{n}','{a}',{c},{e},'{ci}',{t},'{co}','{con}','{per}')".format(f='null',n=username, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, co=correo, con=contraseña, per='user')       
                    cursor.execute(query1)
                    sqlconnection.commit()
                    flash("!Se ha registrado el usuario con éxito")
                    return redirect('/usuarios')
            except:
                flash("!Error! !Los campos Cedula, Edad y Teléfono deben ser valores numéricos")
                return redirect('/usuarios')
            else:
                flash("!Error! !Ya existe un usuario registrado con ese correo electrónico")
                return redirect('/usuarios')
    except:
        flash("!Error al momento de crear el usuario")
        return redirect('/usuarios')

@app.route('/añadir-administrador', methods=["POST", "GET"])
def añadir_administrador():
    try:
        if request.method == "POST":
            username = request.form['nombre']
            apellido = request.form['apellido']
            cedula = request.form['cedula']
            edad = request.form['edad']
            ciudad = request.form['ciudad']
            telefono = request.form['telefono']
            correo = request.form['correo']
            contraseña = generate_password_hash(request.form['contraseña'], method="sha256")

            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            query2 = "SELECT Correo FROM User WHERE Correo='{co}'".format(co=correo)
            cursor.execute(query2)
            data = cursor.fetchall()
            str_data = ''.join(map(str, data))
            electro = "('{a}',)".format(a=correo)
            try:
                if(str_data != electro):
                    query1 = "INSERT INTO User VALUES ({f},'{n}','{a}',{c},{e},'{ci}',{t},'{co}','{con}','{per}')".format(f='null',n=username, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, co=correo, con=contraseña, per='admin')       
                    cursor.execute(query1)
                    sqlconnection.commit()
                    flash("!Se ha registrado el administrador con éxito")
                    return redirect('/administradores')
            except:
                flash("¡Los campos Cédula, Edad y Teléfono deben ser numéricos")
                return redirect('/administradores')
            else:
                flash("Ya existe un administrador registrado con ese correo electrónico")
                return redirect('/administradores')
    except:
        flash("!Error al momento de crear el administrador")
        return redirect('/administradores')

@app.route('/añadir-habitacion', methods=["POST", "GET"])
def añadir_habitacion():
    try:
        if request.method == "POST":
            numero = request.form['numero']
            descripcion = request.form['descripcion']
            disponibilidad = request.form['disponibilidad']
            precio = request.form['precio']

            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            query2 = "SELECT Numero FROM Room WHERE Numero='{n}'".format(n=numero)
            cursor.execute(query2)
            data = cursor.fetchall()
            str_data = ''.join(map(str, data))
            print(str_data)
            electro = "({a},)".format(a=numero)
            print(electro)
            try:
                if(str_data != electro):
                    query1 = "INSERT INTO Room VALUES ({f},{n},'{d}','{dis}',{p})".format(f='null',n=numero, d=descripcion, dis=disponibilidad, p=precio)        
                    cursor.execute(query1)
                    sqlconnection.commit()
                    flash("!Habitación registrada con éxito")
                    return redirect('/habitaciones')
                else:
                    flash("!Error! !Ya existe una habitación registrada con ese número")
                    return redirect('/habitaciones')
            except:
                    flash("!Error! ¡Los campos número y precio deben ser numéricos")
                    return redirect('/habitaciones')
    except:
        flash("!Error al momento de agregar la habitación")
        return redirect('/habitaciones')
        

@app.route('/perfil', methods=["POST", "GET"])
def perfil():
    if 'user' in session  and request.method == "GET": 
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
        cursor.execute(query1)
        user_data = cursor.fetchall()
        return render_template('Mi_perfil.html', users=user_data)
    if 'user' in session  and request.method == "POST":
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            cedula = request.form['cedula']
            edad = request.form['edad']
            ciudad = request.form['ciudad']
            telefono = request.form['telefono']
            clave = generate_password_hash(request.form['contrasena'], method="sha256")            
            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            try:
                query2 = "UPDATE User SET Nombre = '{n}', Apellido = '{a}', Edad = {e}, Ciudad = '{ci}', Telefono ={t}, Contraseña='{cl}' WHERE Cedula = {c}".format(n=nombre, a=apellido, c=cedula, e=edad, ci=ciudad, t=telefono, cl=clave)
                cursor.execute(query2)
                sqlconnection.commit()
                flash("!Usuario editado con éxito")
                return redirect('/perfil')
            except:
                flash("¡Error! !Los campos Cédula, Edad y Teléfono deben ser numéricos")
                return redirect('/perfil')
        except:
            flash("¡Error al momento de actualizar el usuario")
            return redirect('/perfil') 

    else:
        return "No tiene permisos para acceder a la página"

@app.route('/lista-habitaciones')
def lista():
    if 'user' in session :
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
        cursor.execute(query1)
        user_data = cursor.fetchall()
        query2 = "SELECT * FROM Room"
        cursor.execute(query2)
        data = cursor.fetchall()
        return render_template('lista_habitaciones.html', users=user_data, rooms=data)
    else:
        return "No tiene permisos para acceder a la página"
    

@app.route('/lista-habitaciones/<id>')
def reserva(id):
    if 'user' in session:
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT * FROM Room WHERE id = {0}".format(id)
        cursor.execute(query2)
        data = cursor.fetchall()
        sqlconnection.commit()
        query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
        cursor.execute(query1)
        user_data = cursor.fetchall()
        return render_template('reserva.html', rooms = data, users=user_data)
    else:
        return "No tiene permisos para acceder a la página"


@app.route('/calificar/<id>')
def calificacion(id):
    if 'user' in session:
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "SELECT * FROM Room WHERE id = {0}".format(id)
        cursor.execute(query2)
        data = cursor.fetchall()
        sqlconnection.commit()
        query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
        cursor.execute(query1)
        user_data = cursor.fetchall()
        query3 = "SELECT * FROM Score WHERE Id_habitacion={i}".format(i=id)
        cursor.execute(query3)
        comment = cursor.fetchall()
        return render_template('estrellas.html', rooms = data, users=user_data, comments=comment)
    else:
        return "No tiene permisos para acceder a la página"

@app.route('/agregar_calificacion', methods=["POST", "GET"])
def agregar_calificacion():
    try:
        if request.method == "POST":
            comment = request.form["comentario"]
            calificacion_num = request.form["estrellas"]
            id_room = request.form["idr"]
            id_user = request.form["idu"]
            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            try:
                query1 = "INSERT INTO Score VALUES ({i},'{o}',{c},{id},{idu})".format(i='null', o=comment, c=calificacion_num, id=id_room, idu=id_user)
                cursor.execute(query1)
                sqlconnection.commit()
                flash("Calificación añadida con éxito")
                return redirect ("/lista-habitaciones")
            except:
                flash("¡Error! ¡Ha ocurrido un error al momento de añadir el comentario")
                return redirect ("/lista-habitaciones")
    except:
        flash("!Ha ocurrido un error al agregar el comentario")
        return redirect("/lista-habitaciones")

@app.route('/delete-comment/<string:id>')
def eliminar_comentarios(id):
    sqlconnection = sqlite3.Connection("Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "DELETE FROM Score WHERE id = {0}".format(id)
    cursor.execute(query2)
    sqlconnection.commit()
    flash("!Comentario eliminado con éxito")
    return redirect('/lista-habitaciones')

@app.route('/edit-comment/<id>')
def obtener_comentario(id):
    sqlconnection = sqlite3.Connection("Rose.db")
    cursor = sqlconnection.cursor()
    query2 = "SELECT * FROM Score WHERE id = {0}".format(id)
    cursor.execute(query2)
    data = cursor.fetchall()
    sqlconnection.commit()
    query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
    cursor.execute(query1)
    user_data = cursor.fetchall()
    return render_template('editar_comentario.html', comments = data, users=user_data)

@app.route('/update-comment/<id>', methods=["POST"])
def actualizar_comentario(id):
    try:
        if request.method == "POST":
            opinion = request.form['comentario']
            calificacion = request.form['estrellas']
            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            try:
                query2 = "UPDATE Score SET Opinion = '{o}', Calificacion_numerica = {c} WHERE id = {i}".format(o=opinion, c=calificacion, i=id)
                cursor.execute(query2)
                sqlconnection.commit()
                flash("Comentario actualizado con éxito")
                return redirect('/lista-habitaciones')
            except:
                flash("¡Ocurrió un error al momento de actualizar la página")
                return redirect('/lista-habitaciones')
    except:
        flash("¡Ocurrió un error al momento de actualizar la página")
        return redirect('/lista-habitaciones')

@app.route('/mis-reservas')
def reservar():
    if 'user' in session:
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
        cursor.execute(query1)
        user_data = cursor.fetchall()
        return render_template('Mi_reserva.html', users=user_data)
    else:
        return "No tiene permisos para acceder a la página"
        


@app.route('/lista-habitaciones/reserva/reservar', methods=['GET','POST'])
def reservar1():
    try:
        if 'user' in session:
            if request.method == 'POST':
                entrada = request.form["start"]
                salida = request.form["end"]
                sqlconnection = sqlite3.Connection("Rose.db")
                cursor = sqlconnection.cursor()
                query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
                cursor.execute(query1)
                user_data = cursor.fetchall()
                query2 = "SELECT Numero FROM Room WHERE Disponibilidad='{c}'".format(c=True)
                cursor.execute(query2)
                habitacion = cursor.fetchall()
                query4 = "SELECT Fecha_entrada FROM Reservas" 
                cursor.execute(query4)
                fecha_entrada = cursor.fetchall()
                query5 = "SELECT Fecha_salida FROM Reservas" 
                cursor.execute(query5)
                fecha_salida = cursor.fetchall()
                query6 = "SELECT Numero FROM Reservas" 
                cursor.execute(query6)
                Num = cursor.fetchall()
                lista = []
                for i in Num:
                    for j in i:
                        lista.append(j)

                if len(habitacion) != 0: 
                    a = True
                    for j in range(0, len(fecha_entrada)):
                        if ((datetime.strptime(entrada, '%Y-%m-%d')>=datetime.strptime(fecha_entrada[j][0], '%Y-%m-%d') and datetime.strptime(entrada, '%Y-%m-%d')<datetime.strptime(fecha_salida[j][0], '%Y-%m-%d')) or (datetime.strptime(salida, '%Y-%m-%d')>datetime.strptime(fecha_entrada[j][0], '%Y-%m-%d') and datetime.strptime(salida, '%Y-%m-%d')<=datetime.strptime(fecha_salida[j][0], '%Y-%m-%d'))): 
                            a = False
                    for i in range(0, len(habitacion)):
                        if (habitacion[i][0] not in lista or (a==True)):   
                            query3 = "INSERT INTO Reservas VALUES ({n},{c},'{e}','{s}','{co}')".format(n=habitacion[i][0], c=user_data[0][3], e=entrada, s=salida, co=session['user'])       
                            cursor.execute(query3)
                            sqlconnection.commit()
                            flash(f"Reseva exitosa! habitacion {habitacion[i][0]} reservada con exito")
                            return redirect('/lista-habitaciones')
                else:
                        flash("No hay habitaciones disponibles")
                        return redirect('/inicio')
                        
        else:
            return "No tiene permisos para acceder a la página"

    except:
        flash("¡Ocurrió un error al momento de actualizar la página")
        return redirect('/lista-habitaciones')


@app.route('/mis-reservas/reserva', methods=['POST', 'GET'])
def reservas():
    try:
        if 'user' in session:
            sqlconnection = sqlite3.Connection("Rose.db")
            cursor = sqlconnection.cursor()
            query1 = "SELECT * FROM User WHERE Correo='{c}'".format(c=session['user'])
            cursor.execute(query1)
            user_data = cursor.fetchall()
        if request.method == 'POST':
            N_habitacion = request.form["reserv"]
            cedula = request.form["ced"]
            if user_data[0][9] == "user":
                sqlconnection = sqlite3.Connection("Rose.db")
                cursor = sqlconnection.cursor()
                query2 = "SELECT * FROM Reservas WHERE Correo='{c}' and Numero='{n}' and Cedula = {ce}".format(c=session['user'],n=N_habitacion,ce=cedula)
                cursor.execute(query2)
                data = cursor.fetchall()
            if user_data[0][9] == "superadmin" or user_data[0][9] =="admin":
                sqlconnection = sqlite3.Connection("Rose.db")
                cursor = sqlconnection.cursor()
                query2 = "SELECT * FROM Reservas WHERE Numero={n} and Cedula = {ce}".format(n=N_habitacion, ce=cedula)
                cursor.execute(query2)
                data = cursor.fetchone()
            if data:
                return render_template('info_Reserva.html', users=user_data , data=data)
            else:
                flash("No hay reserva asignada o los datos ingresados son erroneos","alert")
                return redirect('/mis-reservas')
        else:
            return "No tiene permisos para acceder a la página"
    except:
        flash("¡Ocurrió un error al momento de actualizar la página")
        return redirect('/mis-reservas')


@app.route('/update-reserva/<string:ced>/<string:Num>', methods=['POST'])
def update_reservas(ced, Num):
    try:
        if 'user' in session:
            if request.method == 'POST':
                N_habitacion = request.form["room"]
                cedula = request.form["cedula"]
                correo = request.form["correo"]
                Fecha_entrada = request.form["Ingreso"]
                Fecha_salida = request.form["Salida"]
                sqlconnection = sqlite3.Connection("Rose.db")
                cursor = sqlconnection.cursor()
                query2 = "UPDATE Reservas SET Numero = {n}, Cedula = {c}, Fecha_entrada = '{fe}', Fecha_salida = '{fs}', correo = '{co}' WHERE Cedula = {Ce} and Numero = {Num}".format(n=N_habitacion, c=cedula, fe=Fecha_entrada, fs= Fecha_salida, co=correo, Ce=ced, Num=Num)
                cursor.execute(query2)
                sqlconnection.commit()
                flash("Se actualizo la reserva")
                return redirect('/mis-reservas')

        else:
            return "No tiene permisos para acceder a la página"
    except:
        flash("¡Ocurrió un error al momento de actualizar la página")
        return redirect('/mis-reservas')

@app.route('/delete-reserva/<string:ced>/<string:Num>')
def delete_reservas(ced, Num):
    if 'user' in session:
        sqlconnection = sqlite3.Connection("Rose.db")
        cursor = sqlconnection.cursor()
        query2 = "DELETE FROM Reservas WHERE Cedula = {Ce} and Numero = {Num}".format(Ce=ced, Num=Num)
        cursor.execute(query2)
        sqlconnection.commit()
        flash("Se elimino el registro")
        return redirect('/mis-reservas')

    else:
        return "No tiene permisos para acceder a la página"
    



if __name__ == "__main__":
    app.run(debug=True)
