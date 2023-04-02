from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
  
app = Flask(__name__)
  
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'employee'
  
mysql = MySQL(app)
  
@app.route('/')

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return redirect(url_for('Index'))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))  
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not name or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (% s, % s, % s)', (name, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
            return render_template('login.html', mesage = mesage)
    else: 
        request.method == 'POST'
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

@app.route('/Index')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM employee_details")
    data = cur.fetchall()
    
    
    cur.close()




    return render_template('index2.html', employee_details=data )


@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        
        id = request.form['id']
        name = request.form['name']
        post = request.form['post']
        salary = request.form['salary']
        cur = mysql.connection.cursor()
        cur.execute("select * from employee_details where id=%s",(id,))
        emp=cur.fetchone()
        if emp:
           flash("id already exist! please enter valid id")
        else:
           flash("Data Inserted Successfully")
           cur.execute("INSERT INTO employee_details (id,name,post,salary) VALUES (%s, %s, %s, %s)", (id, name, post, salary))
           mysql.connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employee_details WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        post = request.form['post']
        salary = request.form['salary']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE employee_details SET name=%s, post=%s, salary=%s WHERE id=%s""", (name, post, salary, id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))





    
if __name__ == "__main__":
    app.run(port=5001,debug=True)
