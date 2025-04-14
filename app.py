from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)
app.secret_key = 'P@55word'

#Create the database model
class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False)
	completed = db.Column(db.Boolean, default=False)

#Home Route
@app.route("/")
def home():
	tasks = Task.query.all()
	return render_template("home.html", tasks=tasks)

#Add Task Route
@app.route("/add", methods=["POST"])
def add():
	task_content = request.form.get("content")
	if task_content:
		new_task = Task(content=task_content)
		db.session.add(new_task)
		db.session.commit()
		flash('Task Added Successfully!')
	return redirect(url_for("home"))

#Delete Task
@app.route("/delete/<int:id>")
def delete(id):
	task_to_delete = Task.query.get_or_404(id)
	db.session.delete(task_to_delete)
	db.session.commit()
	flash('Task Deleted Successfully!')
	return redirect(url_for("home"))

# Complete Task
@app.route("/complete/<int:id>")
def complete(id):
	task = Task.query.get_or_404(id)
	task.completed = not task.completed
	db.session.commit()
	flash('Task updated successfull!')
	return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
