from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'simple_secret'

# Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    category = request.form.get('category')
    price_raw = request.form.get('price')

    # Simple Validations
    if not name or not category:
        flash("Name and Category cannot be empty!")
        return redirect('/')
    try:
        price = float(price_raw)
        if price <= 0:
            flash("Price must be greater than 0!")
            return redirect('/')
    except ValueError:
        flash("Price must be a number!")
        return redirect('/')

    # Save to Database
    new_prod = Product(name=name, category=category, price=price)
    db.session.add(new_prod)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    prod = Product.query.get(product_id)
    db.session.delete(prod)
    db.session.commit()
    return redirect('/')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = Product.query.filter(
        (Product.name.ilike(f"%{query}%")) | (Product.category.ilike(f"%{query}%"))
    ).all()
    return render_template('index.html', products=results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)