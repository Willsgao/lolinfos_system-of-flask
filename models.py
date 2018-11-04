from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 为app指定连接的数据库，并对数据库进行基础数据配置
app.config['SQLALCHEMY_DATABASE_URI']=\
'mysql://root:123456@localhost:3306/myherodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 在数据库命令完成后，自动进行提交操作
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db = SQLAlchemy(app)

# class Users(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(16),nullable=False,unique=True)
#     passwd = db.Column(db.String(32),nullable=False)

#     def __init__(self,username,passwd):
#         self.username = username
#         self.passwd = passwd

#     def __repr__(self):
#         return "<users:%r>"%self.username

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),nullable=False,unique=True)
    password = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(50))
    url = db.Column(db.String(80))
    # source_url = db.Column(db.String(80))
    # # 创建与作品集的反向引用
    # heros = db.relationship('Heros',backref='user',lazy='dynamic')

    def __init__(self,username,password,email=None,url=None):
        self.username = username
        self.password = password
        self.email = email
        self.url = url
        # self.source_url = source_url

    def __repr__(self):
        return "<users:%r>" % self.username

class Heros(db.Model):
    __tablename__ = 'heros'
    id = db.Column(db.Integer,primary_key=True)
    hid = db.Column(db.SmallInteger,nullable=False,unique=True)
    hname = db.Column(db.String(32),nullable=False,unique=True)
    hattack = db.Column(db.String(32),nullable=False)
    hposition = db.Column(db.String(32),nullable=False)
    hbackground = db.Column(db.String(100),nullable=False)
    hgender = db.Column(db.String(16))
    # # 创建与用户名的关联属性
    # user_hid = db.Column(db.Integer,db.ForeignKey('heros.hid'))

    def __init__(self,hid,hname,hattack=None,\
        hposition=None,hbackground=None,hgender=None):
        self.hid = hid
        self.hname = hname
        self.hattack = hattack
        self.hposition = hposition
        self.hbackground = hbackground
        self.hgender = hgender

    def __repr__(self):
        return "<heros:%r>"%self.hname

# 创建数据库
def createdbs():
    try:
        db.create_all()
        return '数据库创建成功'
    except Exception as e:
        return e

# 删除数据库
def dropdbs():
    try:
        db.drop_all()
        return '数据库删除成功'
    except Exception as e:
        return e

# if __name__ == '__main__':
#     # print('执行了么？')
#     res = createdbs()
#     # print('执行了')
#     # print(res)
#     # dropdbs()
#     app.run(debug=True,port=5678)