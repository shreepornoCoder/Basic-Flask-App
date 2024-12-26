from flask import Flask, request, redirect, flash, jsonify
from config import Config
from models import db, Student, Teacher

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def get():
    students = Student.query.all()
    teachers = Teacher.query.all()
    
    return jsonify([{
        'id': student.id,
        'name': student.name,
        'email': student.email,
        'class_name': student.class_name,
        'admitted_at': student.admitted_at,
    } for student in students], 
    [{
        'id':teacher.id,
        'name':teacher.name,
        'subject':teacher.subject,
        'Joining_Date': teacher.join
    }for teacher in teachers]
    )

@app.route('/create/student', methods=['POST'])
def create_student():
    stu_name = request.form['name']
    stu_email = request.form['email']
    stu_class_name = request.form['class_name']

    student = Student(name=stu_name, email=stu_email, class_name=stu_class_name)
    db.session.add(student)

    try:
        db.session.commit()
        flash('Student created successfully!')
    except:
        db.session.rollback()
        flash('Error: Student could not be created!')
    finally:
        return 'Create API called'

@app.route('/create/teacher', methods=['POST'])
def create_teacher():
    teacher_name = request.form['name']
    teacher_subject = request.form['subject']

    teacher = Teacher(name=teacher_name, subject=teacher_subject)
    db.session.add(teacher)

    try:
        db.session.commit()
        flash('Teacher created successfully!')
    except:
        db.session.rollback()
        flash('Error: Teacher could not be created!')
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

@app.route('/delete/student/<int:id>', methods=['DELETE'])
def delete_student(id):
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

@app.route('/delete/teacher/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    
    try:
        db.session.delete(teacher)
        db.session.commit()
        flash('Teacher deleted successfully!')
    except:
        db.session.rollback()
        flash('Error: Teacher could not be deleted!')
    finally:
        return 'Delete API called'

if __name__ == '__main__':
    app.run(debug=True)
