from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #relative path of the database
db = SQLAlchemy(app) #initialize the database

class ToDo(db.Model):
    id = db.Column(db.Integer,primary_key='True')
    content = db.Column(db.String(200),nullable='False')
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        #return '<Task %r>' %self.id
        return (str(self.id) + self.content)


@app.route('/',methods=["POST","GET"])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        print(task_content)
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e.args)
            return "There was an issue adding your task"


    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        print("post query")
        print(tasks)
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Could not delete the task"
    
@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    task_to_update = ToDo.query.get_or_404(id)

    if request.method == "POST":
        
        task_to_update.content = request.form['content']
        
        try:
           
            db.session.commit()
            return redirect('/')
        except:
            return "Update failed"
    else:
        print("imhere to update:",task_to_update.content)
        return render_template("update.html", task=task_to_update)


if __name__== '__main__':
    app.run(debug=True)