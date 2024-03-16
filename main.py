from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, EmailField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


app = Flask(__name__)

class Base(DeclarativeBase):
    pass


csrf = CSRFProtect(app)
bootstrap = Bootstrap5(app)

app.config["SECRET_KEY"] = "blownoutofproportion"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///customer-orders.db"

db = SQLAlchemy(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(25), nullable=True)
    customer_email = db.Column(db.String(25), nullable=True)
    product_category = db.Column(db.String(10), nullable=True)
    product_name = db.Column(db.String(25), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)


#with app.app_context():
    #db.create_all()

# create orderform
class OrderForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = EmailField("Your Email", validators=[DataRequired(), Email()])
    category = SelectField("Product Category", choices=["Cakes", "Cookies", "Bread", "Pastries"], validators=[DataRequired()])
    type = SelectField("Product Name", choices=["CupCakes", "Loaf_Cakes", "Theme_Cake", "OatBran Cookies",
                                                "Gluten-Free Cookies", "Sliced Bread", "Bread Rolls", "Hot-Dog buns",
                                                "Specialty Bread", "Mince Pies"], validators=[DataRequired()] )
    due = DateField("Delivery Date")
    message = TextAreaField("More Details e.g. flavors, quantity, etc")
    send = SubmitField("Submit")


@app.route("/")
def welcome():
    current_year = datetime.now().year
    return render_template("welcome.html", year=current_year)


@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    order_form = OrderForm()
    if order_form.validate_on_submit():
       redirect_url("contact")
    return render_template("contact.html", form=order_form)


if __name__ == "__main__":
    app.run(debug=True)