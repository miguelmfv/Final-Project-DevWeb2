from flask import render_template, flash, redirect, url_for, request

from app import app, db
from app.model.models import Task, Project
from app.templates.forms import TaskForm


@app.route('/tasks/<project_id>', methods=['GET', 'POST'])
def taskList(project_id):
    incomplete_tasks = Task.query.filter_by(project_id=project_id, status=False).order_by(Task.id).all()
    completed_tasks = Task.query.filter_by(project_id=project_id, status=True).order_by(Task.id).all()
    project = Project.query.get_or_404(project_id)
    project_title = project.title
    return render_template('taskList.html', tasks=incomplete_tasks, completed_tasks=completed_tasks, project_id=project_id, project_title=project_title)


@app.route('/tasks/<project_id>/new', methods=['GET', 'POST'])
def newTask(project_id):
    form = TaskForm()
    if form.validate_on_submit():
        print("Validação bem-sucedida!")
        title = form.title.data
        priority = form.priority.data

        task = Task(title=title, priority=priority, project_id=project_id)
        db.session.add(task)
        db.session.commit()
        flash('Tarefa Adicionada!', 'success')
        return redirect(url_for('taskList', project_id=project_id))
    else:
        print("Falha na validação do formulário:", form.errors)
    return render_template('formTask.html', form=form, project_id=project_id)


@app.route('/tasks/<project_id>/edit/<id>', methods=['GET', 'POST'])
def editTask(project_id, id):
    task = Task.query.get_or_404(id)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.priority = form.priority.data

        db.session.commit()
        flash('Tarefa Atualizada!', 'success')
        return redirect(url_for('taskList', project_id=project_id))
    return render_template('formTask.html', form=form)


@app.route('/task/<project_id>/delete/<int:id>', methods=['POST'])
def deleteTask(id, project_id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Tarefa removida!', 'success')
    return redirect(url_for('taskList', project_id=project_id))


@app.route('/tasks/<project_id>/<int:id>/update-status', methods=['POST'])
def updateStatus(project_id, id):
    task = Task.query.get_or_404(id)

    task.status = True if request.form.get('status') == 'on' else False
    db.session.commit()
    flash('Status da tarefa atualizado!', 'success')
    return redirect(url_for('taskList', project_id=project_id))


@app.route('/tasks/<project_id>/showProjectName')
def showProjectName(project_id):
    project = Project.query.get_or_404(project_id)
    return f"{project.title}"
