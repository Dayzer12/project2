from flask import Flask, render_template, request, redirect, session
import sqlite3
app = Flask(__name__)
app.secret_key = 'secret_key'
conn=sqlite3.connect('user.db',check_same_thread=False)
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS user(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT
            )
''')
conn.commit()
cur.execute('''
CREATE TABLE IF NOT EXISTS posts(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            content TEXT,
            author_name TEXT
            )
''')

conn.commit()
 
def add_new_post(title,content,author_name ):
   cur.execute("INSERT INTO posts(name, content, author_name ) VALUES  (?,?,?)", [ title,content,author_name ])
   conn.commit()
def add_user(name,email,password):
    cur.execute('INSERT INTO user(name, email,password)VALUES (?,?,?)',
                [name,email,password])
    conn.commit()

def get_user_by_id(user_id):
    cur.execute(f'SELECT * FROM user WHERE id = {user_id} ')
    return cur.fetchone()

def get_user_by_email(email):
    cur.execute('SELECT * FROM user WHERE email = ?',[email] )
    return cur.fetchone()
@app.route('/')
def main():
    posts = cur.execute('SELECT * FROM posts').fetchall()
    user_name = session.get('user_name')
    return render_template('main.html',posts = posts,user_name = user_name)  

@app.route('/register/', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)
        if user is None:
            add_user(name,email,password)
            session['user_name'] = name
            session['email'] = email
            return redirect('/profile/')
        else:
            print('Такой пользаватель есть')
    return render_template('register.html')
    
@app.route('/login/', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get ('password')
        user = get_user_by_email(email)
        if user is None:
            return render_template('login.html',message= 'Аккаунта  с  такой почты нету')
        if   user[3] == password:
            session['user_name'] = user[1]
            session['email'] = user[2]
            return redirect('/profile/')
        else:
         return render_template ('login.html',message='Пароль неправильный')
    return render_template ('login.html')

@app.route('/profile/',)
def profile():
    return render_template  ('profile.html', name = session['user_name'])
@app.route('/logout/',)
def logout():
    session.clear()
    return redirect('/')

@app.route('/add_post',methods = ['GET','POST'])
def add_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = session.get ('user_name', 'Аноним')

        add_new_post(title,content,author)
        return redirect('/add_post')

    cur.execute('SELECT * FROM posts ORDER BY id DESC')
    posts = cur.fetchall()

    return render_template('add_post.html', posts=posts)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    cur.execute('delete FROM posts WHERE ID = ?',[post_id])
    conn.commit()
    return redirect('/')  

@app.route('/delete_account', methods = [' GET','POST'])
def delete_account():
    name = session.get('user_name')
    cur.execute('delete FROM posts WHERE author_name = ?',[name])
    cur.execute('delete FROM posts WHERE name = ?',[name])
    conn.commit()
    session.clear()
    return redirect ('/')

@app.route('/o_nas/')
def o_nas():
 return  render_template('o_nas.html')

@app.route('/Uslugi/')
def Uslugi():
 return  render_template('Uslugi.html')

@app.route('/Contacts/')
def Contacts():
 return  render_template('Contacts.html')

app.run()


