from flask import Flask,redirect, render_template,url_for,request,flash
import pymysql
import pymysql.cursors
import os 
app=Flask(__name__)

usr="10003"
@app.route('/hello/<int:name>')
def flas(name): 
    sum = 0
    while name > 0 :
        sum+=name%10
        name=name//10

    return "printed %d" %sum
#app.add_url_rule('/',"hello",flas) uncomment if you remove @app.route



@app.route('/home')
def home():
    return render_template('/login.html')
@app.route('/login',methods=['GET','POST'])
def login():
    #error = None
    if request.method == 'POST':
        username=request.form['username']
        
        password=request.form['password']
        if username=='root'and password=='root' :
            return render_template('root_homepage.html')
        con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
        with con:
            cur=con.cursor()
            cur.execute('select employee_id, last_name from employee')

            rows=cur.fetchall()

            for row in rows:
                if row['employee_id']==username and row['last_name']==password:
                    return render_template('emp_homepage.html',usr=username)
              
                
    return render_template('wrong_psswd.html')


@app.route('/emp_deet')
def emp_deet():
    con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
    with con:
        cur=con.cursor()
        cur.execute('select * from employee natural join phone natural join city')

        res=cur.fetchall()
    return render_template ('empdeet.html',result=res,conten_type='application/jason')

@app.route('/prof_deet',methods=['GET','POST'])
def prof_deet():
  if request.method == 'POST':
      usr=request.form['prof_deet']
      con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
      with con:
        cur=con.cursor()
        cur.execute('select employee_id,first_name,last_name,email,qualification,phone_number,project_name from employee natural join phone natural join project natural join partof natural join qualification where employee_id=%s',usr)

        res=cur.fetchall()
  return render_template ('prof_deet.html',result=res,conten_type='application/jason')

@app.route('/pers_deet',methods=['GET','POST'])
def pers_deet():
  if request.method == 'POST':
      usr=request.form['pers_deet']
      con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
      with con:
        cur=con.cursor()
        cur.execute('select employee_id,first_name,last_name,email,qualification,phone_number,project_name from employee natural join phone natural join project natural join partof natural join qualification where employee_id =%s',usr)
        res=cur.fetchall()
  return render_template('pers_deet.html',result=res,conten_type='application/jason')


@app.route('/new_emp',methods=['POST','GET'])
def registration():
    return render_template('registration.html')

@app.route('/reg',methods=['POST','GET'])
def reg():
  if request.method=="POST":
    temp=request.form['id_']
    id_=int(temp )
    bgroup=request.form['bgroup']
    fname=request.form['fname']
    mname=request.form['mname']
    lname=request.form['lname']
    email=request.form['email']
    gender=request.form['gender']
    con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
    with con:
        cur=con.cursor()
        cur.execute('insert into employee (employee_id,first_name,middle_name,last_name,email,gender,blood_group) values(%s,%s, %s,%s , %s,%s,%s)',(id_,fname,mname,lname,email,gender,bgroup))
        con.commit()
  return render_template('success.html')


@app.route('/compare')
def compare():
    return render_template('compare_form.html')


@app.route('/comp_result',methods=['POST','GET'])
def comp_res():
    if request.method == 'POST':
      emp1=request.form['employee1']
      emp2=request.form['employee2']
      emp3=request.form['employee3']
      con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
      with con:
        cur=con.cursor()
        cur.execute('select employee_id,first_name,last_name from employee   where employee_id =%s',emp1)
        res1_1=cur.fetchall()
        cur.execute('select employee_id,qualification from employee natural join  qualification   where employee_id =%s',emp1)
        res1_2=cur.fetchall()
        cur.execute('select employee_id,skill_name from employee natural join skillset natural join has_skillset   where employee_id =%s',emp1)
        res1_3=cur.fetchall()

        cur.execute('select employee_id,first_name,last_name from employee   where employee_id =%s',emp2)
        res2_1=cur.fetchall()
        cur.execute('select employee_id,qualification from employee natural join qualification  where employee_id =%s ',emp2)
        res2_2=cur.fetchall()
        cur.execute('select employee_id,skill_name from employee natural join  skillset natural join has_skillset   where employee_id =%s',emp2)
        res2_3=cur.fetchall()

        cur.execute('select employee_id,first_name,last_name from employee   where employee_id =%s',emp3)
        res3_1=cur.fetchall()
        cur.execute('select employee_id,qualification from employee natural join  qualification   where employee_id =%s',emp3)
        res3_2=cur.fetchall()
        cur.execute('select employee_id,skill_name from employee natural join  skillset natural join has_skillset   where employee_id =%s',emp3)
        res3_3=cur.fetchall()
    return render_template('comp_result.html',result1_1=res1_1,result1_2=res1_2,result1_3=res1_3,result2_1=res2_1,result2_2=res2_2,result2_3=res2_3,result3_1=res3_1,result3_2=res3_2,result3_3=res3_3,emp1=emp1,emp2=emp2,emp3=emp3,conten_type='application/jason')

@app.route('/attend',methods=['POST','GET'])
def attendance():
    if request.method == 'POST':
     employee=request.form['emp']
     con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
     with con:
        cur=con.cursor()
        cur.execute('select employee_id,date_,period from(select employee_id,date_, timediff(out_time,in_time) as period from work_hours where employee_id=%s) as table1' ,employee)
        res=cur.fetchall()
        
    return render_template('attendance.html',result=res,conten_type='application/jason')

@app.route('/update')
def update():
    return render_template('update_emp.html')

@app.route('/emp_pro')
def emp_pro():
    con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
    with con:
        cur=con.cursor()
        cur.callproc('GetEmp')
    res=cur.fetchall()
    return render_template('emp_pro.html',result=res)


@app.route('/update_ph',methods=['GET','POST'])
def update_ph():
    if request.method == "POST" :
        id_=request.form['id_']
        ph=request.form['phone']
        
        con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
        with con:
            cur=con.cursor()
            cur.execute('insert into phone values(%s,%s)',(id_,ph))
            con.commit()

    return render_template('success_update.html')

@app.route('/update_qual',methods=['GET','POST'])
def update_qual():
    if request.method == "POST" :
        id_=request.form['id_']
        qual=request.form['qual']
        
        con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
        with con:
            cur=con.cursor()
            cur.execute('insert into qualification values(%s,%s)',(id_,qual))
            con.commit()

    return render_template('success_update.html')


@app.route('/update_sk',methods=['GET','POST'])
def update_sk():
    if request.method == "POST" :
        id_=request.form['id_']
        sk=request.form['sk']
        
        con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
        with con:
            cur=con.cursor()
            cur.execute('insert into has_skillset values(%s,%s)',(id_,sk))
            con.commit()

    return render_template('success_update.html')

@app.route('/add_to_proj')
def add_to_proj():
    return render_template('add_to_proj.html')

@app.route('/update_proj',methods=['GET','POST'])
def update_proj():
    if request.method=="POST":
        p_id=request.form['proj']
        id_=request.form['id_']
        con= pymysql.connect(host='localhost', user='root', password='Parvathi',db='Project',cursorclass=pymysql.cursors.DictCursor)
        with con:
            cur=con.cursor()
            cur.execute('insert into partof values(%s,%s)',(id_,p_id))
            con.commit()

    return render_template('success_update.html')


if __name__ == '__main__':
    app.run(debug=True)
    app.secret_key = os.urandom(12)