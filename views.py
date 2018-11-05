from flask import Flask,render_template,redirect,\
request,session,make_response
from models import createdbs,dropdbs,Users,Heros,db,app
from dbs_works import DbWorks

# app = Flask(__name__)


# 首页与登录页面为同一个返回页面
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def index_views():
    if request.method == 'GET':
        if 'user' in session:
            return redirect('/dbinfos')
        else:
            if 'user' in request.cookies:
                session['user'] = request.cookies.get('username')
                return redirect('/dbinfos')
            else:
                return render_template('heroindex.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        # 查询用户名是否存在
        user = Users.query.filter_by(username=username).first()
        if not user:
            return '用户名不存在！'
        else:
            if user.password != password:
                return '用户密码输入有误！'
            else:
                resp = redirect('/dbinfos')
                # 创建session
                session['user'] = username
                print('session=',username)
                if 'isSaved' in request.form:
                    print('isSaved+++++++++++++++++')
                    resp.set_cookie('user',username,60*60*24*365)
                    print(request.cookies.get('user'))
                    print('创建cookie!')
                return resp

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
        print('获取信息完毕！')
        # 执行注册用户信息插入数据库操作
        users = Users(username,password,email,url)
        print('准备插入！')
        db.session.add(users)
        print('插入成功！')
        return redirect('/login')

# 信息操作页面
@app.route('/dbinfos',methods=['GET','POST'])
def dbinfos_views():
    if request.method == 'GET':
        return render_template('hero.html')
    else:
        dbs_works = DbWorks(request)
        res = dbs_works.run()
        return res





if __name__ == '__main__':
    app.run(debug=True,port=8888)
