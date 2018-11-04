from flask import Flask,render_template,redirect,request
from models import createdbs,dropdbs,Users,Heros

app = Flask(__name__)


# 首页与登录页面为同一个返回页面
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def index_views():
    if request.method == 'GET':
        return render_template('heroindex.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        # source_url = request.form.get('source_url')        
        # return render_template('index.html')
        return redirect('/dbinfos')

# 创建数据库
# @app.route('/createdbs')
# def createdbs_views():
#     res = createdbs()
#     return res

# 删除数据库
# @app.route('/dropdbs')
# def dropdbs_views():
#     res = dropdbs()
#     return res

# 注册页面
@app.route('/register',methods=['GET','POST'])
def register_views():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 获取注册基本信息
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        url = request.form.get('url')
        # 执行注册用户信息插入数据库操作
        users = Users(username,password,email,url)
        db.session.add(users)
        print('插入成功！')
        return redirect('/login')

# 信息操作页面
@app.route('/dbinfos',methods=['GET','POST'])
def dbinfos_views():
    if request.method == 'GET':
        return render_template('hero.html')
    else:
        pass


if __name__ == '__main__':
    app.run(debug=True,port=8888)
