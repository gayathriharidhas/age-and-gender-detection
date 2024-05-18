from flask import * 
from database import *

admin=Blueprint("admin" ,__name__)


@admin.route('/admhome')
def admhome():

    return render_template("admhome.html")

@admin.route('/viewusers',methods=['get','post'])
def viewuser():

    data={}
    qry="select * from user"
    data['key']=select(qry)
    return render_template('viewuser.html',data=data)

@admin.route('/viewfeedback',methods=['get','post'])
def viewfeedback():

    data={}
    q="select * from feedback inner join user using(user_id)"
    data['key']=select(q)
    return render_template('viewfeedback.html',data=data)

@admin.route('/viewresults',methods={'get','post'})
def viewresult():
    data={}
    a="select * from result inner join user using(user_id)"
    data['key']=select(a)
    return render_template("viewresult.html",data=data)



