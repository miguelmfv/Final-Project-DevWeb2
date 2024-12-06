from io import BytesIO

from flask import render_template, flash, redirect, url_for, send_file, make_response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app import app, db
from app.model.models import Project, Task
from app.templates.forms import ProjectForm


@app.route('/project')
def projectList():
    projects = Project.query.all()
    return render_template('projectList.html', projects=projects)


@app.route('/project/new', methods=['GET', 'POST'])
def newProject():
    form = ProjectForm()
    if form.validate_on_submit():
        cape = form.cape.data
        cape_binario = None
        cape_mimetype = None
        if cape:
            cape_binario = cape.read()
            cape_mimetype = cape.mimetype

        project = Project(title=form.title.data, cape=cape_binario, cape_mimetype=cape_mimetype)
        db.session.add(project)
        db.session.commit()
        flash('Projeto Adicionado!', 'success')
        return redirect(url_for('projectList'))
    return render_template('formProject.html', form=form)


@app.route('/project/edit/<int:id>', methods=['GET', 'POST'])
def editProject(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.title = form.title.data
        cape = form.cape.data
        if cape:
            project.cape = cape.read()
            project.cape_mimetype = cape.mimetype
        db.session.commit()
        flash('Projeto atualizado com sucesso!', 'success')
        return redirect(url_for('projectList'))
    return render_template('formProject.html', form=form)


@app.route('/project/delete/<int:id>', methods=['POST'])
def deleteProject(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Projeto removido com sucesso!', 'success')
    return redirect(url_for('projectList'))


@app.route('/project/<id>')
def showProjectCape(id):
    project = Project.query.get_or_404(id)
    if project.cape:
        return send_file(BytesIO(project.cape), mimetype=project.cape_mimetype)
    flash('Projeto não possui foto.', 'info')
    return redirect(url_for('/'))


@app.route('/project/<project_id>/generateReport')
def generateReport(project_id):
    project = Project.query.get_or_404(project_id)
    completed_tasks = Task.query.filter_by(project_id=project_id, status=True).order_by(Task.id).all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(50, height - 50, "Relatório de Tarefas Concluídas")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 70, f"Projeto: {project.title}")

    pdf.line(50, height - 80, width - 50, height - 80)
    y = height - 120

    pdf.setFont("Helvetica", 12)
    for task in completed_tasks:
        pdf.drawString(50, y, f"ID: {task.id} - Tarefa: {task.title}")
        y -= 20
        if y < 50:
            pdf.showPage()
            y = height - 50

    pdf.setFont("Helvetica-Oblique", 12)
    pdf.drawString(50, 30, "Relatório gerado automaticamente.")
    pdf.drawString(width - 150, 30, "Página 1")

    pdf.save()
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Relatório do projeto: {project.title}.pdf'
    return response