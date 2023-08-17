import os
from flask import Flask,render_template,redirect,request,url_for,flash
from todomodel import db,Todo
from flask_migrate import Migrate
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'datasqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
Migrate(app,db)
tick_count=0
cross_count=0

        
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    all_data = Todo.query.all()
    return render_template('todo.html',todotable=all_data,tick_count=tick_count,cross_count=cross_count,count=tick_count+cross_count)

@app.route('/add',methods=['GET','POST'])
def addTodo():
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(Todo(name))
        db.session.commit()
        return redirect(url_for('index'))
@app.route('/update_count',methods=['GET','POST'])
def updateCount():
    global tick_count,cross_count
    try:
        action = request.form['action']
        if action == 'tick':
            tick_count+=1
        elif action == 'cross':
            cross_count+=1
    except KeyError:
        print("Error: 'action' key is missing in form data")
    return redirect('/')
@app.route('/update_todo/<int:id>/', methods=['GET', 'POST'])
def updateTodo(id):
    mydata = Todo.query.get(id)
    if request.method == 'POST':
        updated_name = request.form['updated_name']
        if mydata:
            mydata.name = updated_name
            db.session.commit()
            return redirect('/')
    return render_template('update_todo.html', item=mydata)


@app.route('/delete_todo/<int:id>/', methods=['GET', 'POST'])
def deleteTodo(id):
    mydata = Todo.query.get(id)
    if request.method == 'POST':
        if mydata:
            db.session.delete(mydata)
            db.session.commit()
            flash("Selected todo has been removed")
            return redirect('/')
    return render_template('delete_todo.html', item=mydata)

   

if __name__ == '__main__':
    app.run(debug=True)
