from flask import Flask, request, flash, redirect, jsonify
from config import Config
from models import db, Student

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET"])
def get():
    students = Student.query.all()

    return jsonify([{
        'id':student.id,
        'name':student.name,
        'email':student.email,
        'class_name':student.class_name,
        "admitted_at":student.admitted_at
    } for student in students])

@app.route('/create', methods=['POST'])
def create():
    name = request.form["name"]
    email = request.form['email']
    class_name = request.form["Class"]

    student = Student(name = name, email = email, class_name = class_name)
    db.session.add(student)

    try:
        db.session.commit()
        flash("Student Created Successfully!")
        return student
    except:
        db.session.rollback()
        flash("Student Couldn't be Created!")


@app.route('/edit/<int:id>', methods=['PUT'])
def edit(id):
    student = Student.query.get_or_404(id)

    student.email = request.email["email"]
    student.class_name = request.email["class_name"]

    try:
        db.session.commit()
        flash("Student Updated Successfully!")
        return student
    except:
        db.session.rollback()
        flash("Student Couldn't be updated!")

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    student = Student.query.get_or_404(id)

    try:
        db.session.delete(student)
        db.session.commit()
        flash("Student Updated Successfully!")
        return student
    except:
        db.session.rollback()
        flash("Student Couldn't be updated!")

if __name__ == "__main__":
    app.run(debug=True)