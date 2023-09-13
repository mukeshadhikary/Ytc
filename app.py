from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ytc.db'
db = SQLAlchemy(app)

class Ytc(db.Model):
    order_no = db.Column(db.String(100), primary_key=True)
    product_name = db.Column(db.String(100), nullable=True)
    product_no = db.Column(db.String(100), nullable=True)
    date_pickup = db.Column(db.String(100), nullable=True)  # Change the data type to String
    suppliers = db.Column(db.String(100), nullable=True)  # Corrected the column name
    name = db.Column(db.String(100), nullable=True)
    qty = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return str(self.order_no)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        order_no = request.form['order_no']
        product_name = request.form['product_name']
        product_no = request.form['product_no']
        date_pickup = request.form['date_pickup']  # Get the date as a string
        suppliers = request.form['suppliers']
        name = request.form['name']
        qty = request.form['qty']
        
        # Create a new Ytc object and add it to the database session
        new_ytc = Ytc(order_no=order_no, product_name=product_name, product_no=product_no,
                      date_pickup=date_pickup, suppliers=suppliers, name=name, qty=qty)
        db.session.add(new_ytc)
        db.session.commit()

        # Show all 20 the Ytc data
        last_20_items = Ytc.query.order_by(Ytc.order_no.desc()).limit(20).all()
        return render_template('index.html', ytc_data=last_20_items[::-1])
        return redirect('/')
    else:
        # Show all 20 the Ytc data
        last_20_items = Ytc.query.order_by(Ytc.order_no.desc()).limit(20).all()
        return render_template('index.html', ytc_data=last_20_items[::-1])
        return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False, port=8080)
