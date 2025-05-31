import os
import uuid
from datetime import datetime, timedelta, UTC
from functools import wraps

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config.from_mapping(
    SECRET_KEY=os.getenv('SECRET_KEY', 'your-secret-key-here'),
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI', 'sqlite:///database.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    UPLOAD_FOLDER='static/avatars',
    JWT_EXPIRATION_MINUTES=30
)

# Initialize extensions
CORS(app)
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False)

class TeacherNode(db.Model):
    __tablename__ = 'teacher_nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    avatar = db.Column(db.String(200))
    school = db.Column(db.String(100))
    details = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('teacher_nodes.id'))
    is_root = db.Column(db.Boolean, default=False)
    children = db.relationship('TeacherNode', backref=db.backref('parent', remote_side=[id]))

# Helper functions
def create_upload_dir():
    """Ensure upload directory exists"""
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def save_uploaded_file(file):
    """Save uploaded file and return filename"""
    if file and file.filename:
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return None

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
            if not current_user:
                raise ValueError('User not found')
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# API Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid request data!'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists!'}), 409
    
    new_user = User(
        public_id=str(uuid.uuid4()),
        username=data['username'],
        password=generate_password_hash(data['password']),
        admin=False
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    print('login')
    
    if not auth or not auth.username or not auth.password:
        print(auth.username)
        print(auth.password)
        return jsonify({'message': 'Could not verify'}), 401
    
    user = User.query.filter_by(username=auth.username).first()
    if not user or not check_password_hash(user.password, auth.password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'public_id': user.public_id,
        'exp': datetime.now(UTC) + timedelta(minutes=app.config['JWT_EXPIRATION_MINUTES'])
    }, app.config['SECRET_KEY'])
    
    return jsonify({'token': token})

@app.route('/tree', methods=['GET'])
@token_required
def get_tree(current_user):
    root_node = TeacherNode.query.filter_by(is_root=True).first()
    if not root_node:
        return jsonify({'message': 'No tree data found!'}), 404
    
    def build_tree(node):
        return {
            'id': node.id,
            'name': node.name,
            'avatar': node.avatar,
            'school': node.school,
            'details': node.details,
            'children': [build_tree(child) for child in node.children]
        }
    
    return jsonify(build_tree(root_node))

@app.route('/teachers/<name>', methods=['GET'])
@token_required
def get_teacher(current_user, name):
    teacher = TeacherNode.query.filter_by(name=name).first()
    if not teacher:
        return jsonify({'message': 'Teacher not found!'}), 404
    
    return jsonify({
        'name': teacher.name,
        'avatar': teacher.avatar,
        'school': teacher.school,
        'details': teacher.details
    })

@app.route('/nodes', methods=['POST'])
@token_required
def add_node(current_user):
    # 权限检查
    # if not current_user.admin:
    #     return jsonify({'message': 'Admin privilege required!'}), 403
    
    # 获取数据
    data = request.form.to_dict()
    print(f"addnode {data}")
    
    # 验证必填字段
    if not data.get('name'):
        print('Name is required!')
        return jsonify({'message': 'Name is required!'}), 400
    if 'parent_id' not in data:
        print('Parent ID is required!')
        return jsonify({'message': 'Parent ID is required!'}), 400
        
    
    # 验证父节点存在
    if data['parent_id']:
        parent = TeacherNode.query.get(data['parent_id'])
        if not parent:
            return jsonify({'message': 'Parent node not found!'}), 404
    
    # 处理文件上传
    avatar = None
    # if 'avatar' in request.files:
    #     avatar_file = request.files['avatar']
    #     if avatar_file and allowed_file(avatar_file.filename):
    #         avatar = save_uploaded_file(avatar_file)
    
    # 创建新节点
    new_node = TeacherNode(
        name=data['name'],
        school=data.get('school', ''),
        details=data.get('details', ''),
        avatar=avatar,
        parent_id=data['parent_id'],
        is_root=not bool(data['parent_id'])
    )
    
    # 数据库操作
    try:
        db.session.add(new_node)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Database error: ' + str(e)}), 500
    
    # 返回响应
    return jsonify({
        'message': 'Node added successfully!',
        'node': {
            'id': new_node.id,
            'name': new_node.name,
            'school': new_node.school,
            'parent_id': new_node.parent_id,
            'is_root': new_node.is_root
        }
    }), 201

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'message': 'Internal server error'}), 500

# Initialize app
with app.app_context():
    create_upload_dir()
    db.create_all()


def create_simple_tree():
    """创建简单的三层师承树"""
    with app.app_context():  # 确保在应用上下文中执行
        try:
            # 清空现有数据
            db.session.query(TeacherNode).delete()
            
            # 创建根节点
            root = TeacherNode(
                name="张三",
                school="哈工大",
                details="哈工大老教师",
                is_root=True
            )
            db.session.add(root)
            db.session.flush()  # 获取ID
            
            # 第一代弟子
            first_gen1 = TeacherNode(
                name="李四",
                school="哈工大",
                details="博导",
                parent_id=root.id
            )
            first_gen2 = TeacherNode(
                name="王五",
                school="哈工大",
                details="哈工大博导",
                parent_id=root.id
            )
            db.session.add_all([first_gen1, first_gen2])
            db.session.flush()
            
            # 第二代弟子
            second_gen1 = TeacherNode(
                name="刘六",
                school="哈工大",
                details="李四博士",
                parent_id=first_gen1.id
            )
            db.session.add(second_gen1)
            
            db.session.commit()
            print("树结构创建成功！")
        except Exception as e:
            db.session.rollback()
            print(f"创建树结构失败: {str(e)}")


if __name__ == '__main__':
    create_simple_tree()
    app.run(debug=True)