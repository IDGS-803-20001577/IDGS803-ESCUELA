from flask import Flask, render_template, Blueprint
from flask import request
from flask import redirect
from flask import url_for

import forms
from flask import jsonify
from config import DevelopmentConfig

from flask_wtf.csrf import CSRFProtect

from models import Maestros
from models import db
from models import Alumnos


app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf_token=CSRFProtect()

@app.route("/",methods=['GET','POST'])
def index():
    create_form=forms.UserForm(request.form)
    if request.method=='POST':
        alum=Alumnos(nombre=create_form.nombre.data,
                apellidos=create_form.apellidos.data,
                email=create_form.email.data)
        db.session.add(alum)
        db.session.commit()
    return render_template('index.html',form=create_form)


@app.route("/indexMaestros",methods=['GET','POST'])
def indexMaestros():
    create_form=forms.UserM(request.form)
    if request.method=='POST':
        maestro = Maestros(nombre=create_form.nombre.data,
                           apellidos=create_form.apellidos.data,
                           email=create_form.email.data,
                           especialidad = create_form.especialidad.data)
        db.session.add(maestro)
        db.session.commit()
    return render_template('indexMaestros.html',form=create_form)

@app.route("/CatalogoAlumnos",methods=['GET','POST'])
def CatalogoAlumnos():
    create_form = forms.UserForm(request.form)
    #select * from alumnos;

    alumnos = Alumnos.query.all()
    return render_template('catalogoAlumnos.html',form=create_form,alumnos=alumnos)

@app.route("/CatalogoMaestros",methods=['GET','POST'])
def CatalogoMaestros():
    create_form = forms.UserM(request.form)

    maestros = Maestros.query.all()
    return render_template('maestros.html',form=create_form,maestros=maestros)

@app.route("/modificar",methods=['GET','POST'])
def modificar():
    create_form=forms.UserForm(request.form)

    if request.method=='GET':
        id=request.args.get('id')
        #select * from alumnos where id=id
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=alum1.id
        create_form.nombre.data=alum1.nombre
        create_form.apellidos.data=alum1.apellidos
        create_form.email.data=alum1.email

    if request.method =='POST':
        id = create_form.id.data
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre = create_form.nombre.data
        alum.apellidos = create_form.apellidos.data
        alum.email = create_form.email.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('CatalogoAlumnos'))
    return render_template('modificar.html',form=create_form)

@app.route("/modificarM",methods=['GET','POST'])
def modificarM():
    create_form=forms.UserM(request.form)

    if request.method=='GET':
        id=request.args.get('id')
        #select * from alumnos where id=id
        maestro=db.session.query(Maestros).filter(Maestros.id==id).first()
        create_form.id.data=maestro.id
        create_form.nombre.data=maestro.nombre
        create_form.apellidos.data=maestro.apellidos
        create_form.email.data=maestro.email
        create_form.especialidad.data=maestro.especialidad

    if request.method =='POST':
        id = create_form.id.data
        mast=db.session.query(Maestros).filter(Maestros.id==id).first()
        mast.nombre = create_form.nombre.data
        mast.apellidos = create_form.apellidos.data
        mast.email = create_form.email.data
        mast.especialidad = create_form.especialidad.data
        db.session.add(mast)
        db.session.commit()
        return redirect(url_for('CatalogoMaestros'))
    return render_template('modificarM.html',form=create_form)

@app.route("/eliminar",methods=['GET','POST'])
def eliminar():
    create_form=forms.UserForm(request.form)

    if request.method=='GET':
        id=request.args.get('id')
        #select * from alumnos where id=id
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=alum1.id
        create_form.nombre.data=alum1.nombre
        create_form.apellidos.data=alum1.apellidos
        create_form.email.data=alum1.email

    if request.method=='POST':
        id=create_form.id.data
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('CatalogoAlumnos'))
    return render_template('eliminar.html',form=create_form)

@app.route("/eliminarM",methods=['GET','POST'])
def eliminarM():
    create_form=forms.UserM(request.form)

    if request.method=='GET':
        id=request.args.get('id')
        #select * from alumnos where id=id
        maestro=db.session.query(Maestros).filter(Maestros.id==id).first()
        create_form.id.data=maestro.id
        create_form.nombre.data=maestro.nombre
        create_form.apellidos.data=maestro.apellidos
        create_form.email.data=maestro.email
        create_form.especialidad.data=maestro.especialidad

    if request.method=='POST':
        id=create_form.id.data
        maestro=db.session.query(Maestros).filter(Maestros.id==id).first()
        
        db.session.delete(maestro)
        db.session.commit()
        return redirect(url_for('CatalogoMaestros'))
    return render_template('eliminarM.html',form=create_form)



if __name__=='__main__':
    db.init_app(app) #Conexión a BD
    with app.app_context():
        db.create_all()
app.run(port=3307)