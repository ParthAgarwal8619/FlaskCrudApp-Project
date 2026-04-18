from flask import Flask, render_template, request ,redirect,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'supersecretkey'


db = SQLAlchemy(app)

class Employee(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.name}"


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # name = request.form['name']
        # email = request.form['email']
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        
        if not name or not email:
            flash("All fields are required!", "danger")
            return redirect("/")

        employee = Employee(name=name, email=email)
        db.session.add(employee)
        db.session.commit()
        
        flash("Employee added successfully!", "success")
        return redirect("/")

    allemployees = Employee.query.all()
    return render_template("index.html", allemployees=allemployees)

@app.route("/delete/<int:sno>")
def delete(sno):
    employee = Employee.query.filter_by(sno=sno).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")
@app.route("/update/<int:sno>",methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        employee = Employee.query.filter_by(sno=sno).first()
        employee.name = name
        employee.email = email
        db.session.add(employee)
        db.session.commit()
        return redirect("/")

    employee = Employee.query.filter_by(sno=sno).first()
    return render_template("update.html", employee=employee)
    




@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)