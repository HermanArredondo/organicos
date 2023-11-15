from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'
bcrypt = Bcrypt(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Modelo de usuario para Flask-Login
class User(UserMixin):
    def __init__(self, user_id, password_hash):
        self.id = user_id
        self.password_hash = password_hash

# Modelo de Comida
class Comida:
    def __init__(self, nombre, precio, imagen):
        self.nombre = nombre
        self.precio = precio
        self.imagen = imagen

# Lista de usuarios con contraseñas cifradas
usuarios = {
    'usuario1': User('usuario1', bcrypt.generate_password_hash('contrasena1').decode('utf-8')),
    'usuario2': User('usuario2', bcrypt.generate_password_hash('contrasena2').decode('utf-8')),
}

@login_manager.user_loader
def load_user(user_id):
    return usuarios.get(user_id)

# Lista de comidas (simplificado, en un entorno real deberías usar una base de datos)
comidas = []

@app.route('/')
def index():
    return render_template('index.html', comidas=comidas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in usuarios:
            user = usuarios[username]
            if bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('admin'))
    
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', comidas=comidas)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/agregar_comida', methods=['POST'])
@login_required
def agregar_comida():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        imagen = request.form['imagen']

        nueva_comida = Comida(nombre=nombre, precio=precio, imagen=imagen)
        comidas.append(nueva_comida)

    return redirect(url_for('admin'))

@app.route('/eliminar_comida/<int:indice>', methods=['GET'])
@login_required
def eliminar_comida(indice):
    if 0 <= indice < len(comidas):
        del comidas[indice]

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
