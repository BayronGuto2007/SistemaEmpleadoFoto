from flask import Flask,render_template,request,redirect,url_for,flash
from flaskext.mysql import MySQL
from flask import send_from_directory  #para cargar las imagenes de la carpeta

from datetime import datetime
import os


app=Flask(__name__,template_folder='template')
app.secret_key = 'Develoteca'

#base de datos
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema'

#Conectandome a la base de datos
mysql.init_app(app)

CARPETA = os.path.join('upload')
app.config['CARPETA']=CARPETA 

@app.route('/upload/<nombreFoto>')
def upload(nombreFoto):
   return send_from_directory(app.config['CARPETA'],nombreFoto)

@app.route("/")
def index():
    sql = "SELECT * FROM `empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit()
    return render_template('empleados/index.html',empleados=empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
    
    conn = mysql.connect()
    cursor = conn.cursor()
    #borrando la foto de la carpeta
    cursor.execute('SELECT foto FROM empleados WHERE id=%s',id)
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
    
    #borrando de la base
    cursor.execute('DELETE FROM empleados WHERE id=%s',(id))
    conn.commit()
    return redirect('/')
 
 
@app.route("/edit/<int:id>")
def edit(id):
    #Conectando a SQL
    conn = mysql.connect()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM empleados WHERE id=%s',(id))
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)
    
@app.route('/create')
def create():
    return render_template('empleados/create.html')
   
@app.route('/store', methods=['POST'])
def storage():
    
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    
    #verificando que llene los campos
    if _nombre == '' or _correo == '' or _foto == '':
        flash('Recuerda llenar los datos de los Campos')
        return redirect(url_for('create'))
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if _foto.filename !="":
        nuevaFoto = tiempo+_foto.filename
        _foto.save('upload/'+nuevaFoto)
    
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    
    datos = (_nombre,_correo,nuevaFoto)
    
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

@app.route('/update', methods=['POST'])
def update():
    #obteniendo los datos
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtId']
    
    #instruccion
    sql = "UPDATE empleados SET nombre= %s,correo=%s WHERE id = %s;"
    
    datos = (_nombre,_correo,id)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if _foto.filename !="":
        nuevaFoto = tiempo+_foto.filename
        _foto.save('upload/'+nuevaFoto)
        
        cursor.execute('SELECT foto FROM empleados WHERE id=%s',id)
        fila=cursor.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute('UPDATE empleados SET foto=%s WHERE id=%s',(nuevaFoto,id))
    
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')
       
if __name__=='__main__':
    app.run(debug=True)






    
   




