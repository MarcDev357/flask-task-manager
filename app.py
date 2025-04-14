from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy import case

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)
app.secret_key = 'P@55word'

#Create the database model
class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False)
	completed = db.Column(db.Boolean, default=False)
	priority = db.Column(db.Integer, default=1) # 1 for low, 2 for medium, 3 for high
	due_date = db.Column(db.Date, nullable=True)

#Home Route
@app.route("/")
def home():
	today = date.today()

	is_overdue = case((Task.due_date < today, True), else_=False)

	tasks = Task.query.order_by(
		Task.completed.asc(),         # Incomplete first
		is_overdue.desc(),            # Overdue first
		Task.due_date.asc().nullslast(),  # Sooner due date first
		Task.priority.desc()          # High → Low
	).all()

	return render_template("home.html", tasks=tasks, current_date=today)

#Add Task Route
@app.route("/add", methods=["POST"])
@app.route("/add", methods=["POST"])
def add():
	task_content = request.form.get("content")
	due_date_str = request.form.get("due_date")
	priority = int(request.form.get("priority", 1))

	due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None

	print("=== New Task Debug ===")
	print("Content:", task_content)
	print("Due Date (str):", due_date_str)
	print("Due Date (parsed):", due_date)
	print("Priority (int):", priority)
	print("======================")

	if task_content:
		new_task = Task(
			content=task_content,
			due_date=due_date,
			priority=priority
		)
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
