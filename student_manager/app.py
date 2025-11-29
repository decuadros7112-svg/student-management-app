from flask import Flask, render_template, request, redirect, url_for, flash, g
from database import get_db, init_db, close_db
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Configuración para Railway
app.config['DATABASE'] = os.environ.get('DATABASE_URL', 'students.db')

@app.before_request
def before_request():
    init_db()

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

# Ruta principal - Consultar todos los registros
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    
    if 'DATABASE_URL' in os.environ:
        cursor.execute('SELECT * FROM students ORDER BY id')
    else:
        cursor.execute('SELECT * FROM students ORDER BY id')
    
    students = cursor.fetchall()
    return render_template('index.html', students=students)

# Consultar registro individual
@app.route('/student/<int:student_id>')
def view_student(student_id):
    db = get_db()
    cursor = db.cursor()
    
    if 'DATABASE_URL' in os.environ:
        cursor.execute('SELECT * FROM students WHERE id = %s', (student_id,))
    else:
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    
    student = cursor.fetchone()
    
    if student is None:
        flash('Estudiante no encontrado', 'error')
        return redirect(url_for('index'))
    
    return render_template('view_student.html', student=student)

# Agregar nuevo registro
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        
        db = get_db()
        cursor = db.cursor()
        
        try:
            if 'DATABASE_URL' in os.environ:
                cursor.execute(
                    'INSERT INTO students (name, email, phone, course) VALUES (%s, %s, %s, %s)',
                    (name, email, phone, course)
                )
            else:
                cursor.execute(
                    'INSERT INTO students (name, email, phone, course) VALUES (?, ?, ?, ?)',
                    (name, email, phone, course)
                )
            
            db.commit()
            flash('Estudiante agregado exitosamente', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error al agregar estudiante: {str(e)}', 'error')
    
    return render_template('add_student.html')

# Editar registro
@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        
        try:
            if 'DATABASE_URL' in os.environ:
                cursor.execute(
                    'UPDATE students SET name = %s, email = %s, phone = %s, course = %s WHERE id = %s',
                    (name, email, phone, course, student_id)
                )
            else:
                cursor.execute(
                    'UPDATE students SET name = ?, email = ?, phone = ?, course = ? WHERE id = ?',
                    (name, email, phone, course, student_id)
                )
            
            db.commit()
            flash('Estudiante actualizado exitosamente', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error al actualizar estudiante: {str(e)}', 'error')
    
    # Obtener datos actuales del estudiante
    if 'DATABASE_URL' in os.environ:
        cursor.execute('SELECT * FROM students WHERE id = %s', (student_id,))
    else:
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    
    student = cursor.fetchone()
    
    if student is None:
        flash('Estudiante no encontrado', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit_student.html', student=student)

# Eliminar registro
@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    db = get_db()
    cursor = db.cursor()
    
    try:
        if 'DATABASE_URL' in os.environ:
            cursor.execute('DELETE FROM students WHERE id = %s', (student_id,))
        else:
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        
        db.commit()
        flash('Estudiante eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar estudiante: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)