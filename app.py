from flask import Flask, request, redirect, flash, jsonify
from config import Config
from models import db, Student

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def get():
    students = Student.query.all()
    # TODO find proper response
    return jsonify([{
        'id': student.id,
        'name': student.name,
        'email': student.email,
        'class_name': student.class_name,
        'admitted_at': student.admitted_at,
    } for student in students])


@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    email = request.form['email']
    class_name = request.form['class_name']

    student = Student(name=name, email=email, class_name=class_name)
    db.session.add(student)

    try:
        db.session.commit()
        flash('Student created successfully!')
    except:
        db.session.rollback()
        flash('Error: Student could not be created!')
    finally:
        return 'Create API called'


@app.route('/edit/<int:id>', methods=['PUT'])
def edit(id):
    student = Student.query.get_or_404(id)
    
    student.email = request.form['email']
    student.class_name = request.form['class_name']
    
    try:
        db.session.commit()
        flash('Student updated successfully!')
    except:
        db.session.rollback()
        flash('Error: Student could not be updated!')
    finally:
        return 'Update API called'

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    student = Student.query.get_or_404(id)
    
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!')
    except:
        db.session.rollback()
        flash('Error: Student could not be deleted!')
    finally:
        return 'Delete API called'


if __name__ == '__main__':
    app.run(debug=True)
