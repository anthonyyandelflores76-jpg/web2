import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secreto_super_seguro_taller_tci")

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Configuración de Base de Datos (Supabase)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

db = SQLAlchemy(app)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    imagen_url = db.Column(db.String(255), nullable=True)

@app.route('/')
def index():
    categoria_seleccionada = request.args.get('categoria')
    if categoria_seleccionada:
        cat_lower = categoria_seleccionada.lower()
        if 'sublimaci' in cat_lower:
            productos = Producto.query.filter(Producto.categoria.ilike('%sublimaci%')).all()
        elif 'papeleri' in cat_lower:
            productos = Producto.query.filter(Producto.categoria.ilike('%papeleri%')).all()
        elif 'cristaleri' in cat_lower:
            productos = Producto.query.filter(Producto.categoria.ilike('%cristaleri%')).all()
        elif 'merchandising' in cat_lower:
            productos = Producto.query.filter(Producto.categoria.ilike('%merchandising%')).all()
        else:
            productos = Producto.query.filter_by(categoria=categoria_seleccionada).all()
    else:
        productos = Producto.query.all()
        
    return render_template('index.html', productos=productos, categoria_activa=categoria_seleccionada)

@app.route('/admin/panel', methods=['GET', 'POST'])
def panel():
    if 'admin_logged' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        categoria = request.form.get('categoria')
        precio = float(request.form.get('precio'))
        descripcion = request.form.get('descripcion')
        
        imagen_url = ""
        archivo = request.files.get('imagen')
        if archivo and archivo.filename != '':
            upload_result = cloudinary.uploader.upload(archivo)
            imagen_url = upload_result.get('secure_url')

        nuevo_producto = Producto(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            descripcion=descripcion,
            imagen_url=imagen_url
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('panel'))

    productos = Producto.query.all()
    return render_template('admin.html', productos=productos)

@app.route('/admin/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'admin_logged' not in session:
        return redirect(url_for('login'))
    
    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        producto.nombre = request.form.get('nombre')
        producto.categoria = request.form.get('categoria')
        producto.precio = float(request.form.get('precio'))
        producto.descripcion = request.form.get('descripcion')
        
        archivo = request.files.get('imagen')
        if archivo and archivo.filename != '':
            upload_result = cloudinary.uploader.upload(archivo)
            producto.imagen_url = upload_result.get('secure_url')

        db.session.commit()
        return redirect(url_for('panel'))

    return render_template('editar.html', producto=producto)

@app.route('/admin/eliminar/<int:id>')
def eliminar(id):
    if 'admin_logged' not in session:
        return redirect(url_for('login'))
    
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('panel'))

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        admin_pass = os.getenv("ADMIN_PASS", "motita2024abc")

        if password == admin_pass:
            session['admin_logged'] = True
            return redirect(url_for('panel'))
        else:
            error = "Contraseña incorrecta."
            
    return render_template('login.html', error=error)

@app.route('/admin/logout')
def logout():
    session.pop('admin_logged', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)