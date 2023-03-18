# Importar librerías necesarias
from flask import Blueprint, request, jsonify, redirect, url_for
import forms 
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from models import Maestros
from db import get_connection

# Crear el blueprint para los maestros
maestros_bp = Blueprint('maestros_bp', __name__)


@maestros_bp.route('/listar')
def listar_maestros():
        connection=get_connection()
        with connection.cursor()as cursor:
            cursor.execute('call consulta_maestros()')
            resulset=cursor.fetchall()
        for row in resulset:
            print(row)
        connection.close()
        return render_template('catalogoMaestros.html')


@maestros_bp.route("/insertarM", methods = ['GET', 'POST'])
def modificarM():
    create_form = forms.MaestForm(request.form)

    if request.method == 'GET':
        id =  request.args.get('id')

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
            # la coma se usa para que lo tome como tupla
                cursor.execute('call consultar_maestro_id(%s)',(id))
                maestro = cursor.fetchall()
                print(maestro)
                print(maestro[0][1])
            
            connection.close()

        except Exception as ex:
            print(ex)

        create_form.id.data = maestro[0][0]
        create_form.nombre.data = maestro[0][1]
        create_form.apellidos.data = maestro[0][2]
        create_form.correo.data = maestro[0][3]
        create_form.especialidad.data = maestro[0][4]
    
    if request.method == 'POST':
        id = create_form.id.data

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
            # la coma se usa para que lo tome como tupla
                cursor.execute('call consultar_maestro_id(%s)',(id,))
                maestro = cursor.fetchall()
                print(maestro)
            
            connection.close()

            #hacer modificacion
            nombre = create_form.nombre.data 
            apellidos = create_form.apellidos.data
            correo = create_form.correo.data
            telefono = create_form.especialidad.data
            print(nombre, type(nombre))
            print(id, type(id))
            print(apellidos, type(apellidos))
            print(telefono, type(telefono))
            #id = str(id)
            #print(id, type(id))
            try:
                connection = get_connection()
                with connection.cursor() as cursor:
                    cursor.execute('call modificar_maestro(%s,%s,%s,%s)',(nombre, apellidos, correo, telefono, id,))
                connection.commit()
                connection.close()

            except Exception as ex:
                print(ex)

        except Exception as ex:
            print(ex)

        return redirect(url_for("maestros.getmaes"))
    
    return render_template("modificarM.html", form = create_form)


@maestros_bp.route('/modificarMaestro', methods=['GET','POST'])
def modificarM():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        maestro = ()
        try:
            con = get_connection()
            with con.cursor() as cursor:
                cursor.execute('call maestroLST(%s)',(id,))
                maestro = cursor.fetchone()
            con.close()
            create_form.id.data = maestro[0]
            create_form.nombre.data = maestro[1]
            create_form.apellidos.data = maestro[2]
            create_form.email.data = maestro[3]
        except Exception as ex:
            print(ex)
    if request.method == 'POST':
        id = create_form.id.data
        try:
            con = get_connection()
            with con.cursor() as cursor:
                cursor.execute('call maestroLST(%s)',(id,))
                maestro = cursor.fetchone()
            con.close()
            maest = Maestros(id = maestro[0],
                            nombre=create_form.nombre.data,
                            apellidos=create_form.apellidos.data,
                            email=create_form.email.data)
            con = get_connection()
            with con.cursor() as cursor:
                cursor.execute('call maestroUPD(%s,%s,%s,%s)',(maest.id,maest.nombre,maest.apellidos,maest.email))
            con.commit()
            con.close()
        except Exception as ex:
            print(ex)
        return redirect(url_for('CatalogoMaestros'))
    return render_template('modificarM.html', form=create_form)
