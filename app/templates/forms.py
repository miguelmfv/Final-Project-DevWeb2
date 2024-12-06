from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Optional
from wtforms import SelectField, SubmitField, StringField, FileField
from flask_wtf.file import FileAllowed

from app.model.models import Project


class ProjectForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    cape = FileField('Capa do Projeto',
                     validators=[Optional(), FileAllowed(['jpg', 'png'], 'Somente arquivos JPG ou PNG!')])
    submit = SubmitField('Salvar')


class TaskForm(FlaskForm):
    title = StringField('Tarefa', validators=[DataRequired()])
    priority = SelectField('Prioridade', validators=[DataRequired()])
    project = SelectField('Projeto', validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def __init__(self):
        super(TaskForm, self).__init__()
        self.priority.choices = ["Urgente", "Alta", "Média", "Baixa"]
        self.project.choices = [(project.id, project.title) for project in Project.query.all()]
