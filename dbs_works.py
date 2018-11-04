from flask import Flask,render_template,redirect,request
from models import createdbs,dropdbs,Users,Heros,db,app
import os
from sqlalchemy import or_

FILE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static'

class DbWorks(object):
    def __init__(self,request):
        self.request = request
        self.order = request.args.get('order')

    def run(self):
        if self.order == 'addall':
            res = self.addall()
            return res
        elif self.order == 'addone':
            res = self.addone()
            return res
        elif self.order == 'change':
            res = self.change()
            return res
        elif self.order == 'search':
            res = self.search()
            return res
        elif self.order == 'delete':
            res = self.delete()
            return res
        else:
            return '请求有误！'

    def addall(self):
        filename = self.request.form.get('hinfo')
        filename = os.path.join(FILE_DIR, filename)
        print(filename)
        with open(filename, 'r') as f:
            num = 0
            print('文件打开了，嘿嘿嘿嘿嘿')
            for line in f:
                print('-----------------------')
                data = line.split('\t')
                print('***********************')
                print(data)
                hid,hname,hattack,hposition,hbackground,hgender =\
                 int(data[0].strip()),data[1].strip(),data[2].strip(),\
                 data[3].strip(),data[4].strip(),data[5].strip()
                try:
                    heroinfos = Heros(hid,hname,hattack,hposition,hbackground,hgender)
                    db.session.add(heroinfos)
                    num +=1
                except Exception as e:
                    print(e)
                    num += 0
        return '成功加入%s条数据'%num        
        

    def addone(self):
        hid,hname,hattack,hposition,hbackground,hgender=\
        self.request.form.get('hid'),self.request.form.get('hname'),\
        self.request.form.get('hattack'),self.request.form.get('hposition'),\
        self.request.form.get('hbackground'),self.request.form.get('hgender')
        try:
            heroinfos = Heros(hid,hname,hattack,hposition,hbackground,hgender)
            db.session.add(heroinfos)
            return '数据添加成功！'
        except Exception as e:
            print(e)
            return '数据添加失败，原因：%s'%e

    def change(self):
        hid,hname,hattack,hposition,hbackground,hgender=\
        self.request.form.get('hid'),self.request.form.get('hname'),\
        self.request.form.get('hattack'),self.request.form.get('hposition'),\
        self.request.form.get('hbackground'),self.request.form.get('hgender')
        try:
            hero = db.session.query(Heros).filter(or_(Heros.hid==hid,Heros.hname==hname)).first()
            hero.hid,hero.hname,hero.hattack,hero.hposition,hero.hbackground,hero.hgender=\
            hid,hname,hattack,hposition,hbackground,hgender
            db.session.add(hero)
            return '数据修改成功！'
        except Exception as e:
            print(e)
            return '数据修改失败，原因：%s'%e

    def search(self):
        try:
            msg = self.request.form.get('hinfo')
            users = db.session.query(Heros).filter(or_(Heros.hid.like('%{}%'.format(msg)),\
                Heros.hname.like('%{}%'.format(msg)),Heros.hattack.like('%{}%'.format(msg)),\
                Heros.hposition.like('%{}%'.format(msg)),Heros.hbackground.like('%{}%'.format(msg)),\
                Heros.hgender.like('%{}%'.format(msg)))).all()
            return render_template('heroinfos.html',msg=msg,users=users)
        except Exception as e:
            print(e)
            return '数据修改失败，原因：%s'%e

    def delete(self):
        dicts = {}
        hid = self.request.form.get('hid')
        hname = self.request.form.get('hname')
        keys = ['hattack','hposition','hbackground','hgender']
        for key in keys:
            if self.request.form.get(key) != '':
                # if key == 'hid':
                    # dicts[key] = int(self.request.form.get(key))
                    # print('dicts[key]',dicts[key])
                dicts[key] = self.request.form.get(key)
        print('dicts=',dicts)

        try:
            wlst = []
            for key in dicts:
                word = 'Heros.%s==%r'%(key,dicts[key])
                wlst.append(word)    
            print('wlst=',wlst)
            words = ','.join(wlst)
            print('words=',words)

            user = db.session.query(Heros).filter(or_(Heros.hid==hid,Heros.hname==hname),"%r"%words).first()
            print('users=',user)
            db.session.delete(user)
            print('users2=',user)
            return '数据删除成功！'
        except Exception as e:
            print(e)
            return '数据删除失败，原因：%s'%e

# dbs_works = DbWorks()
