from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

#Create the database model
class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False)

#Home Route
@app.route("/")
def home():
	tasks = Task.query.all()
	return render_template("home.html", tasks=tasks)

#Add Task Route
@app.route("/add", methods=["POST"])
def add():
	task_content = request.form.get("content")
	print("Received task:", task_content)
	if task_content:
		new_task = Task(content=task_content)
		db.session.add(new_task)
		db.session.commit()
	return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
