from flask import * 
from database import *

public=Blueprint("public" ,__name__)


@public.route('/')
def homepage():
    data={}
    qry="select * from feedback"
    data['feed']=select(qry)
    return render_template("homepage.html",data=data)


@public.route('/login',methods={'get','post'})
def loginpage():
    if 'submit' in request.form:
        username=request.form['username']
        password=request.form['password']

        p="select * from login where username='%s' and password='%s'"%(username,password)
        res=select(p)
        session['lid']=res[0]['login_id']
        if res:
            if res[0]['usertype']=='admin':
                return redirect(url_for('admin.admhome'))
            elif res[0]['usertype']=='user':
                a="select * from user where login_id='%s'"%(session['lid'])
                re=select(a)
                session['uid']=re[0]['user_id']
                return redirect(url_for('user.userhome'))

        print(res)
    return render_template("login.html")

@public.route('/register',methods={'get','post'})
def registerpage():
    if 'submit' in request.form:
        name=request.form['name']
        phone_no=request.form['phone_no']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']

        qry="insert into login values(null,'%s','%s','user')"%(username,password)
        lid=insert(qry)

        qry1="insert into user values(null,'%s','%s','%s','%s')"%(lid,name,phone_no,email)
        insert(qry1)

    return render_template("register.html")

