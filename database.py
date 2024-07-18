from app import app, db, Product

# Create the application context
with app.app_context():
    db.create_all()

    # Add sample products if they don't already exist
    if not Product.query.all():
        db.session.add(Product(name='Chocolate Cake', price=600, image='images/chocolate_cake.jpeg'))
        db.session.add(Product(name='Vanilla Cake', price=500, image='images/vanilla_cake.jpg'))
        db.session.add(Product(name='Strawberry Cake', price=550, image='images/strawberry_cake.jpg'))
        db.session.commit()
