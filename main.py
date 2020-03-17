import pymysql

#from app import app
#from tables import Results
#from db_config import mysql
from flask import *
import os
from flask_table import Table, Col, LinkCol
from flask import flash, render_template, request, redirect
from werkzeug import generate_password_hash, check_password_hash
from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = "secret key"

mysql = MySQL() 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'cruddb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_SOCKET'] = None
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/userregister')
def user_register_view():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def user_register():
    try:
            # conn = None
            # cursor = None
            _name = request.form['uname']
            _email = request.form['email']
            _password = request.form['pass']
            _status = '1'
            role = '1'
            f = request.files['file']
            # validate the received values
            if _name and _email and _password and request.method == 'POST':
                    #do not save password as a plain text
                    _hashed_password = generate_password_hash(_password)
                    # save edits
                    sql = "INSERT INTO users(user_name, user_email, user_password, password_raw, user_profile, user_role, status) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                    data = (_name, _email, _hashed_password, _password,f.filename, role, _status)
                    f.save(os.path.join('D:/learning/python_crud/static/uploads', f.filename))
                    conn = None
                    cursor = None
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql, data)
                    conn.commit()
                    flash('Rgistered successfully!')
                    return redirect('/')
            else:
                    return 'Error while register'
    except Exception as e:
            print(e)
    finally:
            cursor.close() 
            conn.close()

@app.route('/login', methods=['POST'])
def login_user():
    try:
            # conn = None
            # cursor = None
            # _name = request.form['inputName']
            _email = request.form['email']
            _password = request.form['pass']
            # _status = 1
            # validate the received values
            if _email and _password and request.method == 'POST':
                    #do not save password as a plain text
                    _hashed_password = generate_password_hash(_password)
                    # save edits
                    conn = mysql.connect()
                    sql = "SELECT * FROM users WHERE `user_email`='"+_email+"' AND `user_password`='"+_password+"'"
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    cursor.execute("SELECT * FROM users WHERE `user_email`='"+_email+"' AND `password_raw`='"+_password+"'")
                    rows = cursor.fetchone()
                    
                    if rows:
                        session['response']= rows['user_name']
                        session['id']= rows['user_id']
                        session['role']= rows['user_role']
                        if rows['user_role'] == '1':
                            return redirect('/users')
                        else:
                            return redirect('/users_home')
                    else:
                        return "login un successfull"
            else:
                    return 'Someething Went Wrong Please Try Again'

    except Exception as e:
            print(e)
    finally:
            cursor.close() 
            conn.close()

@app.route('/users_home')
def users_home():
    if 'response' and 'id' in session:  
        user_name = session['response'];
        user_id = session['id'];
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE user_id=%s", user_id)
    row = cursor.fetchone()
    return render_template('users_home.html', userdata=row, user_name=user_name, user_id=user_id)

@app.route('/users')
def users():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users ORDER BY `user_id` DESC")
    rows = cursor.fetchall()
    if 'response' and 'id' in session:  
        user_name = session['response'];
        user_id = session['id'];
    # table = Results(rows)
    # table.border = True
    return render_template('users.html', rows=rows, user_name=user_name, user_id=user_id)
    cursor.close() 
    conn.close()

@app.route('/adduser_view')
def adduser_view():
    return render_template('adduser.html')



@app.route('/add', methods=['POST'])
def add():
    try:
            # conn = None
            # cursor = None
            _name = request.form['uname']
            _email = request.form['email']
            _password = request.form['pass']
            _role = request.form['user_role']
            _status = '1'
            f = request.files['file']
            # validate the received values
            if _name and _email and _password and request.method == 'POST':
                    #do not save password as a plain text
                    _hashed_password = generate_password_hash(_password)
                    # save edits
                    sql = "INSERT INTO users(user_name, user_email, user_password, password_raw, user_profile, user_role, status) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                    data = (_name, _email, _hashed_password, _password,f.filename, _role, _status)
                    f.save(os.path.join('D:/learning/python_crud/static/uploads', f.filename))
                    conn = None
                    cursor = None
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql, data)
                    conn.commit()
                    flash('User added successfully!')
                    return redirect('/users')
            else:
                    return 'Error while adding user'
    except Exception as e:
            print(e)
    finally:
            cursor.close() 
            conn.close()

@app.route('/editusers/<int:id>')
def edit_view(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE user_id=%s", id)
    row = cursor.fetchone()
    if 'role' in session:
        user_role = session['role']
    if row:
            return render_template('editusers.html', row=row, user_role=user_role)
    else:
            return 'Error loading #{id}'.format(id=id)
            cursor.close()
            conn.close()

@app.route('/update', methods=['POST'])
def update_user():
    try:        
            _name = request.form['uname']
            _email = request.form['email']
            _password = request.form['pass']
            _id = request.form['id']
            _user_role = request.form['user_role']
            _profile = request.files['file']

            if _profile.filename != '':
                f = _profile
                f.save(os.path.join('D:/learning/python_crud/static/uploads', f.filename))
                file_data = f.filename
            else:
                 f = request.form['user_profile']
                 file_data = f

            if 'role' in session:
                user_role = session['role']
            # validate the received values
            if _name and _email and _password and _id and request.method == 'POST':
                    #do not save password as a plain text
                    _hashed_password = generate_password_hash(_password)
                    # save edits
                    if user_role == '1':
                        sql = "UPDATE users SET user_name=%s, user_email=%s, user_password=%s, password_raw=%s, user_profile=%s, user_role=%s WHERE user_id=%s"
                        data = (_name, _email, _hashed_password, _password, file_data, _user_role, _id,)
                    else:
                        sql = "UPDATE users SET user_name=%s, user_email=%s, user_password=%s, user_profile=%s, password_raw=%s WHERE user_id=%s"
                        data = (_name, _email, _hashed_password, file_data, _password, _id)

                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql, data)
                    conn.commit()
                    flash('User updated successfully!')
                    if user_role == '1':
                        return redirect('/users')
                    else:
                        return redirect('/users_home')                    
            else:
                    return 'Error while updating user'
    except Exception as e:
            print(e)
    finally:
            cursor.close() 
            conn.close()

@app.route('/updateuser_view/<int:id>')
def update_user_view(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE user_id=%s", id)
    row = cursor.fetchone()
    if 'role' in session:
        user_role = session['role']
    if row:
            return render_template('updateuser.html', row=row, user_role=user_role)
    else:
            return 'Error loading #{id}'.format(id=id)
            cursor.close()
            conn.close()

@app.route('/user_update', methods=['POST'])
def userupdate():
    try:        
            _name = request.form['uname']
            _email = request.form['email']
            _password = request.form['pass']
            _id = request.form['id']
            # validate the received values
            if _name and _email and _password and _id and request.method == 'POST':
                _hashed_password = generate_password_hash(_password)
                sql = "UPDATE users SET user_name=%s, user_email=%s, user_password=%s, password_raw=%s WHERE user_id=%s"
                data = (_name, _email, _hashed_password, _password, _id)

                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                flash('User updated successfully!')
                return redirect('/users_home')                
                    
            else:
                    return 'Error while updating user'
    except Exception as e:
            print(e)
    finally:
            cursor.close() 
            conn.close()

@app.route('/delete/<int:id>')
def delete_user(id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE user_id=%s", (id,))
            conn.commit()
            flash('User deleted successfully!')
            return redirect('/users')
    except Exception as e:
            print(e)
    finally:
            cursor.close() 
            conn.close()

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



if __name__ == "__main__":
    app.run()