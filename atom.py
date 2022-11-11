# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        proyecto Atom
# Purpose:
#
# Author:      Ruben Machado
#
# Created:     18/05/2020
# Copyright:   (c) Ruben Machado 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from werkzeug.utils import secure_filename
from os import path, mkdir
import os
import sqlite3

cwd = os.getcwd()  # Obtenemos el directorio de trabajo actual (CWD)
files = os.listdir(cwd)  # Obtenemos todos los archivos en ese directorio
#print("Files in %r: %s" % (cwd, files))

app = Flask(__name__)
app.config['SECRETKEY'] = 'secretkey'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

#conexion con el servidor
#funcion que se encargara de recuperar datos de la base
def recuperar(query):
    with sqlite3.connect("comim.db") as conn:
        cursor = conn.cursor()
        result = cursor.execute(query).fetchall()
        conn.commit()
    return result

#funcion que se ecnargara de guardar datos en la base
def guardar_datos(query, parametros = ()):
    with sqlite3.connect("comim.db") as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parametros)
        conn.commit()
    return result

#Funcion que se encargara de borrar datos de la base
def eliminar(query):
    with sqlite3.connect("comim.db") as conn:
        cursor = conn.cursor()
        result = cursor.execute(query)
        conn.commit()

#funcion para verificar campos
def verificar_campos(listado):
    listaFinal = []
    for campo in listado:
        if(len(campo) == 0):
            listaFinal.append(campo)

    return len(listaFinal) == 0

#verifica si el capo contiene numeros
def numero(numero):
    try:
        int(numero)
        return True
    except:
        return False

@app.route('/')
def index():
    if session.get('legajo'):
        return redirect(url_for('main'))
    else:
        return render_template('index.html')

@app.route('/entrar')
def entrar():
    if session.get('legajo'):
        return redirect(url_for('main'))
    else:
        return render_template('index.html')

@app.route('/entrar/config', methods=['POST'])
def entrar_config():
    if request.method == 'POST':
        legajo = request.form['legajo']
        codigo = request.form['codigo']
        lista = [legajo, codigo]
        if(verificar_campos(lista)):
            if(numero(legajo)):
                query = "SELECT * FROM privilegios WHERE matricula='{}'".format(legajo)
                datos = recuperar(query)
                if(datos):
                    if(codigo == datos[0][3]):
                        session['legajo'] = legajo
                        session['nombre'] = datos[0][1]
                        session['apellido'] = datos[0][2]
                        return redirect(url_for('main'))
                    else:
                        flash("La Contraseña no es Correcta")
                else:
                    flash("El Administrador No Esta Registrado")
            else:
                flash("Completa el Campo Legajo con numeros Enteros")
        else:
            flash("Debes Completar Todos los Campos")
            
    return render_template('index.html')

@app.route('/main')
def main():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        return render_template('main.html')

@app.route("/categoriaAntiguedad")
def categoriaDocente():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        return render_template('categoriaDocente.html')

@app.route("/categoriaAntiguedad/config", methods=['POST'])
def categoriaDocente_config():
    rec = request.form['antiguedad']
    antiguedad = int(rec)

    if(antiguedad <= 4):
        flash("Categoria 1 - $69.68")
    elif(antiguedad >= 5 and antiguedad <= 8):
        flash("Categoria 2 - $74.26")
    elif(antiguedad >= 9 and antiguedad <= 12):
        flash("Categoria 3 - $79.98")
    elif(antiguedad >= 13 and antiguedad <= 16):
        flash("Categoria 4 - $85.72")
    elif(antiguedad >= 17 and antiguedad <= 20):
        flash("Categoria 5 - $92.38")
    elif(antiguedad >= 21 and antiguedad <= 24):
        flash("Categoria 6 - $98.99")
    elif(antiguedad >= 25):
        flash("Categoria 7 - $108.82")

    return redirect(url_for('categoriaDocente'))

@app.route('/notificaciones')
def noticias():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        return render_template('notificaciones.html')

@app.route('/list')
def listado():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query = "SELECT * FROM infoPersonal"
        datos = recuperar(query)
        return render_template('listado.html', tripulantes=datos)
    
@app.route('/anexo1')
def anexo1():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        voluntarios = "SELECT * FROM listadoMaterias"
        rec_voluntarios = recuperar(voluntarios) #listado tal cual como esta en la base

        nuevaLista = []
        lista = puntajesTotales()

        for i in rec_voluntarios:
            #if(len(i[3]) != 0 ):
            listado = []
            filtro = str(i[3]).split()
            id = i[0]
            punto = id.index(".")
            new_id = id[0:punto] + ".0"
            rec = recuperar(f"SELECT cursos FROM listadoMaterias WHERE id='{new_id}'")
            titulo = rec[0][0]

            for e in filtro:
                cedula = recuperar(f"SELECT cedula FROM infoPersonal WHERE legajo='{e}'")

                for r in lista:
                    try:
                        a = int(r[6])
                        if(a < 1):
                            categoria = 0
                        elif(a >= 1 and a <= 4):
                            categoria = 1
                        elif(a >= 5 and a <= 8):
                            categoria = 2
                        elif(a >= 9 and a <= 12):
                            categoria = 3
                        elif(a >= 13 and a <= 16):
                            categoria = 4
                        elif(a >= 17 and a <= 20):
                            categoria = 5
                        elif(a >= 21 and a <= 24):
                            categoria = 6
                        elif(a >= 25):
                            categoria = 7
                    except:
                        pass

                    if(f"{e}" == f"{r[0]}"):
                        agregar = [categoria, r[8], cedula[0][0], r[3], r[4], r[1], r[2], i[1]]
                        listado.append(agregar)

            listado.sort(reverse=True)

            contador = 1
            for e in listado:
                e.insert(0, contador)
                contador += 1

            puntajes = []
            for a in listado:
                puntajes.append(a[2])

            try:
                ret_puntaje = max(puntajes)
            except:
                pass

            for f in listado:
                if f[2] == ret_puntaje:
                    f.insert(8, "(T)")
                else:
                    f.insert(8, "(S)")

            nuevaLista.append([titulo, listado])  
    
                
        return render_template('anexo1.html', tripulantes=nuevaLista)

@app.route('/listadosCorreos')
def mails():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        sql = "SELECT correo FROM otrosDatos"
        rec = recuperar(sql)

        return render_template('correos.html', correos=rec)

@app.route('/resultadoConcurso')
def resultadosDeConcurso():
    if not session.get('legajo'):
        return redirect(url_for('legajo'))
    else:
        voluntarios = "SELECT * FROM listadoMaterias"
        rec_voluntarios = recuperar(voluntarios) #listado tal cual como esta en la base

        nuevaLista = []
        lista = puntajesTotales()

        for i in rec_voluntarios:
            #if(len(i[3]) != 0 ):
            listado = []
            filtro = str(i[3]).split()   
            for e in filtro:
                cedula = recuperar(f"SELECT cedula FROM infoPersonal WHERE legajo='{e}'")
                for r in lista:
                    grado = 1
                    if(f"{e}" == f"{r[0]}"):
                        try:
                            antiguedad = int(r[6])
                            if(antiguedad <= 4):
                                grado = 1
                            elif(antiguedad >= 5 and antiguedad <= 8):
                                grado = 2
                            elif(antiguedad >= 9 and antiguedad <= 12):
                                grado = 3
                            elif(antiguedad >= 13 and antiguedad <= 16):
                                grado = 4
                            elif(antiguedad >= 17 and antiguedad <= 20):
                                grado = 5
                            elif(antiguedad >= 21 and antiguedad <= 24):
                                grado = 6
                            elif(antiguedad >= 25):
                                grado = 7

                        except: pass

                        agregar = [r[8], r[3], r[4], grado, r[1], cedula[0][0]]
                        listado.append(agregar)

            listado.sort(reverse=True)

            contador = 1
            for e in listado:
                e.insert(0, contador)
                contador += 1

            for r in listado:
                if(r[0] == 1):
                    r.insert(6, "TITULAR")
                else:
                    r.insert(6, "SUPLENTE")
    
            nuevaLista.append([i[0], i[1], i[2], listado])  

        return render_template('resultadoConcurso.html', tripulantes=nuevaLista)


@app.route('/listadosGenerales')
def listados_generales():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query2 = "SELECT * FROM listadoMaterias"
        listadoGen = recuperar(query2)

        nuevaLista = []
        for i in listadoGen:
            filtro = str(i[3]).split() 
            cantidad = len(filtro)
            if cantidad > 0:
                cantidad = len(filtro)
            else:
                cantidad = ""
            nuevaLista.append([str(i[0]), str(i[1]), str(i[2]), str(cantidad)])
    
        #este codigo es para actualizar los datos en la base de datos 
        #con el personal voluntario que se postulo para las materias
        query3 = "SELECT * FROM materias"
        todos = recuperar(query3)

        """
        conexion = sqlite3.connect('comim.db')
        cursor = conexion.cursor()
    
        contador = 0
        for materias in todos:
            filtro = str(materias[1]).split() 
            for datos in filtro:
                sql = "SELECT * FROM listadoMaterias WHERE id='{}'".format(datos)
                rec = cursor.execute(sql).fetchone()
                voluntarios = []
                try:
                    voluntarios.append(rec[3] + " " + str(materias[0]))
                    texto = "".join(voluntarios)
                    cursor.execute(f"UPDATE listadoMaterias SET voluntarios='{texto}' WHERE id='{rec[0]}'")
                    conexion.commit()
                    contador += 1
                    print(contador)
                except:
                    print("Error")

        conexion.close()
        """
        
        return render_template('todosLosCursos.html', tripulantes=nuevaLista)

@app.route('/puntajeDeVoluntarios')
def puntajes():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        sql = "SELECT legajo, grado, especialidad, nombre1, apellido1, antiguedadDocente FROM infoPersonal"
        rec = recuperar(sql)

        conexion = sqlite3.connect('comim.db')
        cursor = conexion.cursor()

        listado = []
        for i in rec:
            rec2 = cursor.execute(f"SELECT * FROM cursos WHERE legajo='{i[0]}'").fetchall()
            totalCursos = len(rec2)
            try:
                entero = int(i[5])
            except: pass

            antiguedad = round(entero / 3 )
            total = totalCursos + entero + antiguedad
            listado.append([i[0], i[1], i[2], i[3], i[4], totalCursos, i[5], antiguedad, total])

        conexion.close()

        datos = {"info": listado}

        return render_template('puntajesDeVoluntarios.html', tripulantes=datos)

def puntajesTotales():
    sql = "SELECT legajo, grado, especialidad, nombre1, apellido1, antiguedadDocente FROM infoPersonal"
    rec = recuperar(sql)

    conexion = sqlite3.connect('comim.db')
    cursor = conexion.cursor()

    listado = []
    for i in rec:
        rec2 = cursor.execute(f"SELECT * FROM cursos WHERE legajo='{i[0]}'").fetchall()
        totalCursos = len(rec2)
        try:
            entero = int(i[5])
        except: pass

        antiguedad = round(entero / 3 )
        total = totalCursos + entero + antiguedad
        listado.append([i[0], i[1], i[2], i[3], i[4], totalCursos, i[5], antiguedad, total])

    conexion.close()

    return listado

@app.route('/cantidadDeVoluntariosTotales')
def voluntariosTotales():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        voluntarios = "SELECT * FROM listadoMaterias"
        rec_voluntarios = recuperar(voluntarios) #listado tal cual como esta en la base

        nuevaLista = []
        lista = puntajesTotales()

        for i in rec_voluntarios:
            listado = []
            filtro = str(i[3]).split()   
            for e in filtro:
                for r in lista:
                    if(f"{e}" == f"{r[0]}"):
                        agregar = [r[8], r[3], r[4], r[1]]
                        listado.append(agregar)

            listado.sort(reverse=True)

            contador = 1
            for e in listado:
                e.insert(1, contador)
                contador += 1
    
            nuevaLista.append([i[0], i[1], i[2], listado])  

        return render_template('totalDeVoluntarios.html', tripulantes=nuevaLista)

@app.route('/cantitdadDeVoluntarios/<numero>')
def cantidadVoluntarios(numero):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        
        return render_template('cantidadVoluntarios.html', tripulantes=None)


@app.route('/new')
def agregar():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        return render_template('notificaciones.html')

@app.route('/new/config', methods=['POST'])
def new_config():
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    elif request.method == 'POST':
        legajo = request.form['legajo']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha']
        genero = request.form['genero']
        listado = [legajo, nombre, apellido, fecha]
        if(verificar_campos(listado)):
            if(numero(legajo)):
                query = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(legajo)
                dato = recuperar(query)
                if not(dato):
                    listado = [legajo, 'MP', 'IM', nombre, "", apellido, "", genero, fecha, "", 'ESIM', None, "", "", "", "", "", ""]
                    query = "INSERT INTO infoPersonal VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                    guardar_datos(query, listado)
                    mkdir("static/img/imgDigitalizadas/{}".format(legajo))
                    flash("Tripulante Agregado con exito")
                    return redirect(url_for('agregar'))
                else:
                    flash("El Legajo ingresado ya esta Registrado como {} {}".format(dato[0][3], dato[0][5]))
            else:
                flash("Por Favor Completa el Campo Legajo con Numeros Enteros")
        else:
            flash("Debes Completar Todos los Campos")
    
    return render_template('agregar.html')

@app.route('/perfil/<matricula>/documentosDigitalizados')
def docDigitalizados(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query1 = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        query2 = "SELECT * FROM docDigitalizados WHERE legajo='{}'".format(matricula)
        rec1 = recuperar(query1)
        rec2 = recuperar(query2)
        dato = {"info": rec1[0], "imagenes": rec2}
        return render_template('perfil/doc_Digitalizados.html', tripulante=dato)

@app.route('/perfil/<matricula>/documentosDigitalizados/config', methods=['POST'])
def docDigitalizados_config(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    elif request.method == 'POST':
        dirFoto = request.files['perfil']
        filename = secure_filename(dirFoto.filename)
        listado = (matricula, filename)
        if(dirFoto):
            app.config['UPLOAD_FOLDER'] = './static/img/imgDigitalizadas/{}/'.format(matricula)
            dirFoto.save(path.join(app.config['UPLOAD_FOLDER'], filename))
            query = "INSERT INTO docDigitalizados VALUES(?,?)"
            guardar_datos(query, listado)
            flash("Imagen Subida con Exito")
            return redirect(url_for('docDigitalizados', matricula=matricula))
        else:
            flash("Selecciona una Foto antes de Guardar")
            return redirect(url_for('docDigitalizados', matricula=matricula))

@app.route('/perfil/<matricula>/load_perfil')
def load_perfil(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        rec = recuperar(query)
        dato = {"info": rec[0]}
        return render_template('perfil/cambiarFoto.html', tripulante=dato)

@app.route('/perfil/<matricula>/load_perfil/config', methods=['POST'])
def load_perfil_config(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    elif request.method == 'POST':
        dirFoto = request.files['perfil']
        filename = secure_filename(dirFoto.filename)
        if(dirFoto):
            query = (f"UPDATE infoPersonal SET foto_perfil='{filename}' WHERE legajo='{matricula}'" )
            guardar_datos(query)
            app.config['UPLOAD_FOLDER'] = './static/img/imgDigitalizadas/{}/'.format(matricula)
            dirFoto.save(path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Foto de Perfil Actualizada con Exito")
            return redirect(url_for('load_perfil', matricula=matricula))
        else:
            flash("Selecciona una Foto antes de Guardar")
            return redirect(url_for('load_perfil', matricula=matricula))

@app.route('/perfil/<matricula>/infoPersonal')
def infoPersonal(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        rec = recuperar(query)
        dato = {"info": rec[0]}
        return render_template('perfil/infoPersonal.html', tripulante=dato)

@app.route('/perfil/<matricula>/editInfoPersonal')
def editInfoPersonal(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        rec = recuperar(query)
        dato = {"info": rec[0]}
        return render_template('edit/editInfoPersonal.html', tripulante=dato)

@app.route('/perfil/<matricula>/editInfoPersonal/config', methods=['POST'])
def editInfoPersonal_config(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    elif request.method == 'POST':
        nombre1 = request.form['nombre1']
        nombre2 = request.form['nombre2']
        apellido1 = request.form['apellido1']
        apellido2 = request.form['apellido2']
        grado = request.form['grado']
        especialidad = request.form['especialidad']
        genero = request.form['genero']
        compania = request.form['compania']
        seccion = request.form['seccion']
        lugar_nacimiento = request.form['lugar_nacimiento']
        fecha_nacimiento = request.form['fecha_nacimiento']
        fecha_ingreso = request.form['fecha_ingreso']
        credencial_serie = request.form['credencial_serie']
        credencial_numero = request.form['credencial_numero']
        cedula = request.form['cedula']
        antiguedadDocente = request.form['antiguedadDocente']

        conexion = sqlite3.connect('comim.db')
        cursor = conexion.cursor()
        cursor.execute(f"UPDATE infoPersonal SET grado='{grado}', especialidad='{especialidad}', nombre1='{nombre1}', nombre2='{nombre2}', apellido1='{apellido1}', \
                apellido2='{apellido2}', genero='{genero}', fecha_nacimiento='{fecha_nacimiento}', compania='{compania}', seccion='{seccion}', lugar_nacimiento='{lugar_nacimiento}', \
                fecha_ingreso='{fecha_ingreso}', credencial_serie='{credencial_serie}', credencial_numero='{credencial_numero}', cedula='{cedula}', antiguedadDocente='{antiguedadDocente}' \
                WHERE legajo='{matricula}'" )
        conexion.commit()
        conexion.close()

        return redirect(url_for('infoPersonal', matricula=matricula))

@app.route('/perfil/<matricula>/imprimir')
def imprimir(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        sql1 = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        sql2 = "SELECT * FROM otrosDatos WHERE legajo='{}'".format(matricula)
        sql3 = "SELECT * FROM cursos WHERE legajo='{}'".format(matricula)
        infopersonal = recuperar(sql1) #23 datos 
        otrosdatos = recuperar(sql2) #23 datos
        cursos = recuperar(sql3)
        if(otrosdatos):
            datos = {"info": infopersonal[0], "otros": otrosdatos[0], "cursos": cursos}
            return render_template('perfil/imprimir.html', tripulante=datos)
        else:
            datos = {"info": infopersonal[0], "otros": None, "cursos": None}
            return render_template('perfil/imprimir.html', tripulante=datos)

@app.route('/perfil/<matricula>/imprimir_materias')
def imprmir_materias(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query1 = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        query2 = "SELECT * FROM materias WHERE legajo='{}'".format(matricula)
        query3 = "SELECT * FROM listadoMaterias"
        sql2 = "SELECT * FROM otrosDatos WHERE legajo='{}'".format(matricula)
        otrosdatos = recuperar(sql2) #23 datos
        rec1 = recuperar(query1)
        rec2 = recuperar(query2)
        rec3 = recuperar(query3)
        if(rec2):
            #le sacamos los espacios al listado de cursos
            filtro = str(rec2[0][1]).split()
            materias = []

            horas = []
            for i in filtro:
                for e in rec3:
                    if e[0] == i:
                        horas.append(e[2])

            horasTotales = 0
            for i in horas:
                horasTotales += i

            #creamos un filtro para los titulos de los cursos
            cursos = []
            for i in filtro:
                a = i.index('.')
                cursos.append(i[0:a] + ".0")

            #agregamos los titulos al listado general
            for i in cursos:
                if i not in filtro:
                    filtro.append(i)

            #convertimos la lista de str a flotantes para poder ordenarlos
            flotantes = []
            for i in filtro:
                a = repr(i)
                flotantes.append(a)

            #ordenamos la lista
            ordenados = sorted(flotantes)
            
            #volvemos a convertir la lista en str para conpararlos ocn la base
            listaTexto = []
            for i in ordenados:
                a = str(i[1:-1])
                listaTexto.append(a)

            #Hacemos un recorrido con el listado general para obtener los nombres de las materias
            for i in listaTexto:
                for e in rec3:
                    if e[0] == i:
                        materias.append((e[0], e[1], e[2]))
                        break
        else:
            materias = rec2

        dato = {"info": rec1[0], "otros": otrosdatos[0], "materias": materias, "horas": horasTotales}
        return render_template('perfil/imprimir_materias.html', tripulante=dato)

@app.route('/perfil/<matricula>/otrosDatos')
def otrosDatos(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        sql1 = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        sql2 = "SELECT * FROM otrosDatos WHERE legajo='{}'".format(matricula)
        infopersonal = recuperar(sql1) #23 datos 
        otrosdatos = recuperar(sql2) #23 datos
        if(otrosdatos):
            datos = {"info": infopersonal[0], "otros": otrosdatos[0]}
            return render_template('perfil/otrosDatos.html', tripulante=datos)
        else:
            datos = {"info": infopersonal[0], "otros": None}
            return render_template('perfil/otrosDatos.html', tripulante=datos)

@app.route('/perfil/<matricula>/editOtrosDatos')
def editOtrosDatos(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        sql1 = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        sql2 = "SELECT * FROM otrosDatos WHERE legajo='{}'".format(matricula)
        infopersonal = recuperar(sql1) #23 datos
        otrosdatos = recuperar(sql2) #23 datos

        if(otrosdatos):
            datos = {"info": infopersonal[0], "otros": otrosdatos[0]}
            return render_template('edit/editOtrosDatos.html', tripulante=datos)
        else:
            datos = {"info": infopersonal[0], "otros": None}
            return render_template('edit/editOtrosDatos.html', tripulante=datos)

@app.route('/perfil/<matricula>/editOtrosDatos/config', methods=['POST'])
def editOtrosDatos_config(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    elif request.method == 'POST':
        fecha_ascenso = request.form['fecha_ascenso']
        ven_carne = request.form['vencimiento_CarneSalud']
        dir_completa = request.form['direccion_Completa']
        prof_diplomado = request.form['profecion_Diplomado']
        celular = request.form['celular']
        telefono = request.form['telefono']
        correo = request.form['correo']

        listado = [matricula, fecha_ascenso, ven_carne, dir_completa, prof_diplomado, celular, telefono, correo]

        #primero recuperamos los datos
        sql = "SELECT * FROM otrosDatos WHERE legajo='{}'".format(matricula)
        dato = recuperar(sql)
        if (dato):
            conexion = sqlite3.connect('comim.db')
            cursor = conexion.cursor()

            cursor.execute(f"UPDATE otrosDatos SET fecha_ultimoAscenso='{fecha_ascenso}', vencimiento_carneSalud='{ven_carne}',\
                direccion_completa='{dir_completa}', profecion_diplomado='{prof_diplomado}', celular='{celular}', telefono='{telefono}', correo='{correo}' WHERE legajo='{matricula}'")

            conexion.commit()
            conexion.close()

            return redirect(url_for('otrosDatos', matricula=matricula))
        else:
            sql = "INSERT INTO otrosDatos VALUES(?,?,?,?,?,?,?,?)"
            guardar_datos(sql, listado)
            return redirect(url_for('otrosDatos', matricula=matricula))

@app.route('/perfil/<matricula>/infoCursos')
def infoCursos(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query1 = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        query2 = "SELECT * FROM cursos WHERE legajo='{}' ORDER BY desde".format(matricula)
        rec2 = recuperar(query2)
        rec1 = recuperar(query1)
        dato = {"info": rec1[0], "cursos": rec2}
        return render_template('perfil/infoCursos.html', tripulante=dato)

@app.route('/perfil/<matricula>/infoCursosNuevo')
def infoCursos_nuevo(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        rec = recuperar(query)
        dato = {"info": rec[0]}
        return render_template('edit/nuevoCurso.html', tripulante=dato)

@app.route('/perfil/<matricula>/infoCursosNuevo/config', methods=['POST'])
def infoCursos_nuevo_config(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    elif request.method == 'POST':
        desde = request.form['desde']
        hasta = request.form['hasta']
        unidad = request.form['unidad']
        sigla = request.form['sigla']
        descripcion = request.form['descripcion']
        nota = request.form['nota']
        listado = [matricula, desde, hasta, unidad, sigla, descripcion, nota]
        listado_config = [matricula, unidad, sigla, descripcion]
        if(verificar_campos(listado_config)):
            query = "INSERT INTO cursos VALUES(NULL,?,?,?,?,?,?,?)"
            guardar_datos(query, listado)
            flash("Datos almacenados con exito")
            return redirect(url_for('infoCursos_nuevo', matricula=matricula))
        else:
            flash("Debes completar todos los campos")
    return redirect(url_for('infoCursos_nuevo', matricula=matricula))

@app.route('/perfil/<matricula>/infoCursosEdit/<numero>')
def infoCursosEdit(matricula, numero):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query1 = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        query2 = "SELECT * FROM cursos WHERE id='{}'".format(numero)
        rec2 = recuperar(query2)
        rec1 = recuperar(query1)
        dato = {"info": rec1[0], "cursos": rec2[0]}
        return render_template('edit/editInfoCursos.html', tripulante=dato)

@app.route('/perfil/<matricula>/infoCursosEdit/<numero>/config', methods=['POST'])
def infocursosEdit_config(matricula, numero):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    elif request.method == 'POST':
        desde = request.form['desde']
        hasta = request.form['hasta']
        unidad = request.form['unidad']
        sigla = request.form['sigla']
        descripcion = request.form['descripcion']
        nota = request.form['nota']
        conexion = sqlite3.connect('comim.db')           
        cursor = conexion.cursor()
        cursor.execute(f"UPDATE cursos SET desde='{desde}', hasta='{hasta}', unidad='{unidad}', sigla='{sigla}', curso='{descripcion}', nota='{nota}' WHERE id='{numero}'")
        conexion.commit()
        conexion.close()
        return redirect(url_for('infoCursos', matricula=matricula))

@app.route('/perfil/<matricula>/infoCursosEdit/<numero>/deleted')
def infoCursosEliminar(matricula, numero):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        sql = "DELETE FROM cursos WHERE id='{}'".format(numero)
        eliminar(sql)
        return redirect(url_for('infoCursos', matricula=matricula))

@app.route('/nombramiento')
def nombramiento():
    
    todos = recuperar(f"SELECT * FROM materias")
    listado = []

    for i in todos:
        datos = recuperar(f"SELECT legajo, grado, especialidad, nombre1, apellido1 FROM infoPersonal WHERE legajo='{i[0]}'")
        for e in datos:
            legajo = str(i[0])
            agregar = titulares(legajo)
            for r in agregar:
                id = r[0]
                punto = id.index(".")
                new_id = id[0:punto] + ".0"
                rec = recuperar(f"SELECT cursos FROM listadoMaterias WHERE id='{new_id}'")
                titulo = rec[0][0]
                try:
                    espacio = titulo.index("\"")
                    r.insert(5, titulo[0:espacio])
                except: pass

            guardar = [e[4], e[1], e[2], e[3], e[0], agregar] #apellido, grado, especialidad, nombre, legajo, listado de materias -> List
            listado.append(guardar)

    listado.sort()
    contador = 0
    for y in listado:
        contador += 1
        y.insert(0, contador)

    return render_template('nombramiento.html', tripulantes=listado)

def listadoGeneral() -> list:
    voluntarios = "SELECT * FROM listadoMaterias"
    rec_voluntarios = recuperar(voluntarios) #listado tal cual como esta en la base

    nuevaLista = []
    lista = puntajesTotales()
    for i in rec_voluntarios:
        listado = []
        filtro = str(i[3]).split()   
        for e in filtro:
            for r in lista:
                if(f"{e}" == f"{r[0]}"):
                    #puntaje, nombre, apellido, legajo
                    agregar = [r[8], r[3], r[4], r[0]]
                    listado.append(agregar)

        listado.sort(reverse=True)

        #le agregamos el puesto en el que quedo Titular o Suplente
        #retorna puntaje, puesto, nombre, apellido
        contador = 0
        for e in listado:
            e.insert(1, contador)
            contador += 1

        nuevaLista.append([i[0], i[1], i[2], listado])

    return nuevaLista

def titulares(matricula):
    query2 = "SELECT * FROM materias WHERE legajo='{}'".format(matricula)
    query3 = "SELECT * FROM listadoMaterias"
    rec2 = recuperar(query2)
    rec3 = recuperar(query3)
    general = listadoGeneral()

    if(rec2):

        #le sacamos los espacios al listado de cursos
        filtro = str(rec2[0][1]).split()
        materias = []

        #listado con las materias y los titulos
        #retorna num, materia, horas
        for i in filtro:
            for e in rec3:
                if e[0] == i:
                    materias.append([e[0], e[1], e[2]])
                    break

        #seccion que se encaga de recuperar si el tripulante es titular o suplente
        for r in range(len(materias)):
            materia = materias[r][0]
            for g in general:
                if(g[0] == materia):
                    for f in g[3]:
                        if(str(f[-1]) == matricula):
                            if(f[1] > 0 ): 
                                materias[r].insert(4, f"SUP")
                            else: 
                                materias[r].insert(4, f"TIT")
        
        return materias
                

@app.route('/perfil/<matricula>/listadoCursosPostula')
def list_cursosPostula(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query1 = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        query2 = "SELECT * FROM materias WHERE legajo='{}'".format(matricula)
        query3 = "SELECT * FROM listadoMaterias"
        rec1 = recuperar(query1)
        rec2 = recuperar(query2)
        rec3 = recuperar(query3)
        general = listadoGeneral()

        if(rec2):
            #le sacamos los espacios al listado de cursos
            filtro = str(rec2[0][1]).split()
            materias = []

            horas = []
            for i in filtro:
                for e in rec3:
                    if e[0] == i:
                        horas.append(e[2])

            horasTotales = 0
            for i in horas:
                horasTotales += i

            #creamos un filtro para los titulos de los cursos
            cursos = []
            for i in filtro:
                a = i.index('.')
                cursos.append(i[0:a] + ".0")

            #agregamos los titulos al listado general
            for i in cursos:
                if i not in filtro:
                    filtro.append(i)

            #convertimos la lista de str a flotantes para poder ordenarlos
            flotantes = []
            for i in filtro:
                a = repr(i)
                flotantes.append(a)

            #ordenamos la lista
            ordenados = sorted(flotantes)
            
            #volvemos a convertir la lista en str para conpararlos ocn la base
            listaTexto = []
            for i in ordenados:
                a = str(i[1:-1])
                listaTexto.append(a)

            #listado con las materias y los titulos
            #retorna num, materia, horas
            for i in listaTexto:
                for e in rec3:
                    if e[0] == i:
                        materias.append([e[0], e[1], e[2]])
                        break

            #seccion que se encaga de recuperar si el tripulante es titular o suplente
            for r in range(len(materias)):
                materia = materias[r][0]
                for g in general:
                    if(g[0] == materia):
                        for f in g[3]:
                            if(str(f[-1]) == matricula):
                                if(f[1] > 0 ): 
                                    materias[r].insert(4, f"S ({f[1]})")
                                else: 
                                    materias[r].insert(4, f"T")
        
        else:
            materias = rec2
            horasTotales = 0

        dato = {"info": rec1[0], "materias": materias, "horas": horasTotales}
        return render_template('perfil/listadoCursosPostula.html', tripulante=dato)

@app.route('/perfil/<matricula>/cursosPostula')
def cursosPostula(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query1 = "SELECT * FROM infoPersonal WHERE legajo='{}'".format(matricula)
        rec1 = recuperar(query1)
        dato = {"info": rec1[0]}
        return render_template('perfil/cursosPostula.html', tripulante=dato)

@app.route('/perfil/<matricula>/cursosPostula/config', methods=['POST'])
def cursosPostula_config(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    elif request.method == 'POST':
        materias = request.form['listado']
        listado = [matricula, materias]
        query = "INSERT INTO materias VALUES(?,?)"
        guardar_datos(query, listado)
        return redirect(url_for('list_cursosPostula', matricula=matricula))

@app.route('/perfil/<matricula>/deleted')
def eliminarPerfil(matricula):
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        query = "DELETE FROM infoPersonal WHERE legajo='{}'".format(matricula)
        eliminar(query)
        query = "DELETE FROM otrosDatos WHERE legajo='{}'".format(matricula)
        eliminar(query)
        query = "DELETE FROM cursos WHERE legajo='{}'".format(matricula)
        eliminar(query)
        query = "DELETE FROM materias WHERE legajo='{}'".format(matricula)
        eliminar(query)
        return redirect(url_for('listado'))

@app.route('/privilegios')
def privilegios():  
    if not session.get('legajo'):
        return redirect(url_for('entrar'))
    else:
        return render_template('privilegios.html')

@app.route('/salir') 
def salir():
    session['legajo'] = None
    session['nombre'] = None

    session['apellido'] = None
    return redirect(url_for('entrar'))

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
