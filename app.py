from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)

DB_FILE = "tasks.txt"


def read_tasks():
    tasks = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            for line in f:
                task_id, title, completed = line.strip().split(",")
                tasks.append({
                    "id": int(task_id),
                    "title": title,
                    "completed": bool(int(completed))
                })
    return tasks


def write_tasks(tasks):
    with open(DB_FILE, "w") as f:
        for task in tasks:
            f.write(f"{task['id']},{task['title']},{int(task['completed'])}\n")


@app.route('/')
def home():
    tasks = read_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add():
    tasks = read_tasks()
    new_task_id = max([task["id"] for task in tasks], default=0) + 1
    task_title = request.form["task"]

    new_task = {
        "id": new_task_id,
        "title": task_title,
        "completed": False
    }
    tasks.append(new_task)
    write_tasks(tasks)

    return redirect(url_for('home'))


@app.route('/delete/<task_id>', methods=['GET', 'POST'])
def delete(task_id):
    tasks = read_tasks()
    tasks = [task for task in tasks if task["id"] != int(task_id)]
    write_tasks(tasks)
    return redirect(url_for('home'))


@app.route('/complete/<task_id>', methods=['GET', 'POST'])
def complete(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task["id"] == int(task_id):
            task["completed"] = not task["completed"]
    write_tasks(tasks)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)