from flask import Flask,flash,render_template ,session, redirect,session,request,send_from_directory,url_for #post y get
from flask_uploads import UploadSet,IMAGES,configure_uploads

from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import SubmitField
import re
import roya 

# roya.diagnosticar(roya.file_url)
# def funcion1():
#     b="retorno"
#     return b

app=Flask(__name__)
app.config['SECRET_KEY']='1234567890'
app.config['UPLOADED_PHOTOS_DEST']='uploads'

photos=UploadSet('photos',IMAGES)
configure_uploads(app,photos)

class UploadForm(FlaskForm):
    photo=FileField(
        validators=[
            FileAllowed(photos,"only images are allowed"),
            FileRequired("file was empty")
        ]        
    )
    submit=SubmitField("Diagnosticar")

    
# Un "middleware" que se ejecuta antes de responder a cualquier ruta. Aquí verificamos si el usuario ha iniciado sesión
@app.before_request
def antes_de_cada_peticion():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if not 'usuario' in session and ruta != "/login" and not ruta.startswith("/static"):
        flash("Inicia sesión para continuar")
        return redirect("/login")
    # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar



@app.route('/uploads/<filename>')    
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)


# @app.route('/')

@app.route('/home')
def index():
    titulo="SCANPLANT"
    pie="saludo"
    
    return  render_template("index.html",t1=titulo,p1=pie)

@app.route('/')
@app.route('/login', methods= ["GET", "POST"])
def login():
    titulo="SCANPLANT"
    pie="saludo"
    no_valido = "" 
    valido="Ingresa tus datos"
    email=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if password == "1234" and email == "user@example.com":
            session["usuario"] = email
            return redirect("/home")
        else:
            no_valido="correo o contraseña no validos"
            
            return render_template("login.html",t1=titulo,p1=pie, no_valido=no_valido,valido=valido)
    else:
        return render_template("login.html",t1=titulo,p1=pie,valido=valido)


@app.route('/sign_out')
def sign_out():
    session.clear()
    return redirect("/login")

@app.route('/busqueda',methods=['GET','POST'])
def upload_image():
    titulo="SCANPLANT"
    pie="nuevo"

    form =UploadForm()
    # session.clear()
  
    if form.validate_on_submit():
        filename=photos.save(form.photo.data)  
        file_url=url_for('get_file',filename=filename)
        # c=file_url
        
        c=roya.diagnosticar(file_url)
        
        # c = re.sub('[/]', '', c)
    else:
        file_url=None
        c=""
    return  render_template("busqueda.html",form=form,file_url=file_url,t1=titulo,p1=pie,c=c)


if __name__ =='__main__': #luego de ir a produccion ya no es necesario
    app.run (port=5000 , debug=True)
    
    