from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# Create database
with app.app_context():
    db.create_all()

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']

        if task_content:
            new_task = Task(content=task_content)
            db.session.add(new_task)
            db.session.commit()

        return redirect('/')

    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

# Delete task
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect('/')

# Edit task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        db.session.commit()

        return redirect('/')

    return render_template('index.html', edit_task=task, tasks=Task.query.all())

if __name__ == '__main__':
    app.run(debug=True)