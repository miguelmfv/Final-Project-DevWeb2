from app import db


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(10), nullable=True)
    status = db.Column(db.Boolean, nullable=False, default=False)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', back_populates='tasks')

    def __repr__(self):
        return f'<Task {self.title}>'


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    cape = db.Column(db.LargeBinary, nullable=True)
    cape_mimetype = db.Column(db.String(50), nullable=True)

    tasks = db.relationship('Task', back_populates='project', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.title}>'
