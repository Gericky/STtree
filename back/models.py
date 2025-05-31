from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean, default=False)

class TeacherNode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200))
    school = db.Column(db.String(100))
    details = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('teacher_node.id'))
    is_root = db.Column(db.Boolean, default=False)
    
    # 自引用关系
    children = db.relationship('TeacherNode', backref=db.backref('parent', remote_side=[id]))