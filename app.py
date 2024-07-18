from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

class OrderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Place Order')

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/order/<int:product_id>', methods=['GET', 'POST'])
def order(product_id):
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(name=form.name.data, address=form.address.data, product_id=product_id)
        db.session.add(order)
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('index'))
    product = Product.query.get_or_404(product_id)
    return render_template('order.html', product=product, form=form)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
