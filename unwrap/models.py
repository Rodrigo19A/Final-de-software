from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user
from datetime import datetime

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia esto por una clave segura
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de extensiones
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Modelo de Usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Carga el usuario por ID

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cart = db.relationship('Cart', backref='buyer', lazy=True)

    def add_to_cart(self, product_id):
        item_to_add = Cart(product_id=product_id, user_id=self.id)
        db.session.add(item_to_add)
        db.session.commit()
        flash('Your item has been added to your cart!', 'success')

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}', '{self.id}')"

# Modelo de Productos
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Products('{self.name}', '{self.price}')"

# Modelo de Carrito
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Cart('Product id:{self.product_id}', 'id: {self.id}', 'User id:{self.user_id}')"

# Creación de tablas
with app.app_context():
    db.create_all()

# Función para obtener detalles de inicio de sesión
def getLoginDetails():
    if current_user.is_authenticated:
        return f"User: {current_user.firstname}, Items in cart: {len(current_user.cart)}"
    else:
        return "User not logged in."

# Ruta principal
@app.route("/")
def home():
    noOfItems = getLoginDetails()
    return f"Welcome to the Flask App! {noOfItems}"

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app.run(debug=True)
