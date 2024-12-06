from io import BytesIO

from flask import render_template, send_file, flash, redirect, url_for, send_from_directory
from app import app
from app.model.models import Project


@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/<project_id>')
def showCape(project_id):
    project = Project.query.get_or_404(project_id)
    if project.cape:
        return send_file(BytesIO(project.cape), mimetype=project.cape_mimetype)
    flash('Projeto não possui foto.', 'info')
    return redirect(url_for('/'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(directory='static', path='app', mimetype='image/V2 - Branco.png')
