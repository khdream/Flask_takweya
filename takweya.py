from flask import Flask, request, jsonify, render_template, redirect, flash, url_for, session, make_response, Response
from pymongo import MongoClient
import os
import sys
import urllib
import time
from passlib.apps import custom_app_context as pwd_context
from flask import session as login_session
from datetime import datetime
from bson import ObjectId
from bson.json_util import dumps
import gridfs
from werkzeug import secure_filename
from flask_mail import Mail, Message
from PIL import Image
import json
import urllib3
import xmltodict
from collections import defaultdict 
from vclass import makeAPIClass
import paypalrestsdk
from paypalrestsdk import Payout, ResourceNotFound
import functools
import math
import pymongo
import phonenumbers
import re
import random
from flask_mail import Mail, Message
import string
from urllib.parse import urlparse
from flask_pymongo import PyMongo
UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "Ass@nkoya12"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
dir = os.path.abspath(os.path.dirname(__file__))
user = "admin"
pwd = "admin123"
# connect to db
try:
    client = MongoClient("mongodb://"+user+":"+pwd+"@localhost:27017/")
    #client = MongoClient('mongodb://localhost:27017/')
    db = client['takweya']
    print("connected to mongodb successfully!")
except:
    print("Unable to connect to database")
    sys.exit(1)

try:
    db_students = db["students"]
    db_teachers = db["teachers"]
    db_is_loggedin = db["is_loggedin"]
    db_questions = db["questions"]
    db_sessions = db["sessions"]
    db_transactions = db["transactions"]
    db_withdraws = db["withdraws"]
except:
    print("Unable to connect to collections")
    sys.exit(1)

try:
    fs = gridfs.GridFS(db)
except:
    print("Unable to connect to GridFS")
    sys.exit(1)

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.office365.com',
    MAIL_PORT=587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME='noreply@takweya.com',
    MAIL_PASSWORD='Email@Takweya13%',
    MAIL_DEFAULT_SENDER = 'support@takweya.com'
)
mail = Mail(app)
'''
paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "Ae30W_Flmr9KBnopPU6u2_mHqp2llnaJcXTtdZdoUH6K7o5GAsQiZ846-IrbWPwYdsBg7AxFpK4L_Vy0",
  "client_secret": "EApEqQaU4D2zLqIG0vpnHezICyYkLeLTtBE_3xku4in0SZEwA-ukyeM4EITe1OxUMOa1-WPtoRgzoRbz" })

'''
paypalrestsdk.configure({
  "mode": "live", # sandbox or live
  "client_id": "AeHvVviaTdKxdWlRrULt2QVp_R8QvFoKFnlzNgTkMxA0-s9INSr832ig8zZvM0FXkJFRISf-18Pu2gm7",
  "client_secret": "ELTwW1R5-wogY0h2Ohjb_nDnmWsHkM75jPvXZqQ5f4cxH6ytwXkpA2dxmrmtQ5cPVQRMiMkyTwmPJ6WT" })

def slogin_check(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if checkLogin('student') == False:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return secure_function

def tlogin_check(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if checkLogin('teacher') == False:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return secure_function

def alogin_check(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if checkLogin('admin') == False:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return secure_function


def checkLogin(job):
    if 'user_id' not in session or session['job'] != job:
        return False
    user_id = session['user_id']
    if job == 'student':
        someone = db_students.find_one({"_id": ObjectId(user_id)})
    elif job == 'teacher':
        someone = db_teachers.find_one({"_id": ObjectId(user_id)})
    elif job == 'admin':
        someone = True
    if someone == None:
        return False
    else:
        return True

def send_mail_template():
    if request.method == "GET":
        qmail = Message("Welcome to Takweya!",
                        sender="noreply@takweya.com",
                        recipients=['zadahmed@outlook.com']) #Change this to recipent 
        qmail.html = render_template('email.html') # add name for the html when sending email :- If you check the html it shows Congratulations "Name" replace Name with the name of the person who signed up 
        mail.send(qmail)
        return 'Done'



def sendemail_signup(data):
    print("----------send singup email--------")
    print(data)
    qmail = Message("Welcome to Takweya!", sender="noreply@takweya.com", recipients=[data['email']])
    qmail.html = render_template('email-signup.html', data=data)
    try:
        mail.send(qmail)
    except TimeoutError as e:
        print(e)
        return False
    except:
        print("unexpected error while sending email.")
        return False
    return True

def sendemail_accept(data):
    print("----------send accept email--------")
    print(data)
    qmail = Message("Welcome to Takweya!", sender="noreply@takweya.com", recipients=[data['email']])
    qmail.html = render_template('email-accept.html', data=data)
    try:
        mail.send(qmail)
    except TimeoutError as e:
        print(e)
        return False
    except:
        print("unexpected error while sending email.")
        return False
    return True

def sendemail_help(data):
    print("----------send help email--------")
    print(data)
    qmail = Message("Report", sender="noreply@takweya.com", recipients=['noreply@takweya.com'])
    qmail.html = render_template('email-help.html', data=data)
    try:
        mail.send(qmail)
    except TimeoutError as e:
        print(e)
        return False
    except:
        print("unexpected error while sending email.")
        return False
    return True

def sendemail_invoice(data):
    print("----------send invoice email--------")
    print(data)
    qmail = Message("Report", sender="noreply@takweya.com", recipients=[data['email']])
    qmail.html = render_template('email-invoice.html', data=data)
    try:
        mail.send(qmail)
    except TimeoutError as e:
        print(e)
        return False
    except:
        print("unexpected error while sending email.")
        return False
    return True

def sendemail_newquestion(data):
    print("----------send new question email--------")
    print(data)
    for item in data:
        qmail = Message("New question", sender="noreply@takweya.com", recipients=[item['email']])
        qmail.html = render_template('email-newquestion.html', data=item)
        try:
            mail.send(qmail)
        except TimeoutError as e:
            print(e)
            return False
        except:
            print("unexpected error while sending email.")
            return False
    return True

@app.route("/email-accept")
def email_accept():
    user={'name': 'test'}
    return render_template('email-accept.html', data=user)

@app.route("/email-help")
def email_help():
    user={'name': 'test', 'msg': 'Here is Report'}
    return render_template('email-help.html', data=user)

@app.route("/email-signup")
def email_singup():
    user={'name': 'test', 'job':'teacher'}
    return render_template('email-signup.html', data=user)

@app.route("/email-newquestion")
def email_newquestion():
    user={'name': 'test', 'question': 'question content'}
    return render_template('email-newquestion.html', data=user)

@app.route("/email-invoice")
def email_invoice():
    user={'name': 'test', 'session_length': '23:34', 'teacher_rate': '20 AED per hour', 'service_charge': '20 AED', 'Total': '200AED'}
    return render_template('email-invoice.html', data=user)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/ar")
def homear():
    return render_template('arindex.html')

@app.route("/aboutus")
def aboutus():
    return render_template('about-us.html')

@app.route("/contactus")
def contactus():
    return render_template('contact-us.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route('/admin', methods=['GET'])
@alogin_check
def admin_page():
    total_sessions = db_sessions.find({}).count()
    students = db_students.find({})
    teachers = db_teachers.find({})
    total_teachers = db_teachers.find({}).count()
    total_revenue = 0
    total_students = students.count()
    agr = [ {'$group': {'_id': { '$dateToString': { 'format': "%Y-%m-%d", 'date': "$Date Signed Up" } }, 'count': { '$sum': 1 } } } ]
    student_list = list(db_students.aggregate(agr))
    teacher_list = list(db_teachers.aggregate(agr))
    temp = defaultdict(list)  
    if len(student_list) > 0:
        for elem in student_list: 
            temp[elem['_id']].extend(str(elem['count'])) 
    if len(teacher_list) > 0:
        for elem in teacher_list: 
            temp[elem['_id']].extend(str(elem['count']))
    sign_up_list = []
    for x,y in temp.items():
        temp_dict = []
        cnt = 0
        for item in y:
            cnt += int(item)
        temp_dict.append(str(x))
        temp_dict.append(str(cnt))
        sign_up_list.append(temp_dict)
    agr = [ {'$group': {'_id': { '$dateToString': { 'format': "%Y-%m-%d", 'date':{ '$dateFromString':{'dateString': "$Start Time",'format': "%d/%m/%Y, %H:%M:%S"} }} }, 'Tutor_Time': { '$sum': '$Duration' },'count': { '$sum': 1 },'balance': { '$sum': '$Price paid' } } } ]
    temp_sessions = list(db_sessions.aggregate(agr))
    session_list = []
    avg_session_list = []
    revenue_list = []
    if len(temp_sessions) > 0:
        for item in temp_sessions:
            temp = []
            temp1 = []
            rev_temp = []
            temp.append(str(item['_id']))
            temp.append(str(round(item['Tutor_Time']/60,2)))
            temp1.append(str(item['_id']))
            temp1.append(str(round(item['Tutor_Time']/(item['count']*60), 2)))
            rev_temp.append(str(item['_id']))
            rev_temp.append(str(round(item['balance'],2)))
            total_revenue += round((item['balance']*0.2)/1.1, 2)
            session_list.append(temp)
            avg_session_list.append(temp1)
            revenue_list.append(rev_temp)
    all_data = {"total_sessions":total_sessions, 'total_teachers':total_teachers,'total_students':total_students,
                'total_revenue':total_revenue,"session_list":session_list,"avg_session_list":avg_session_list,
                "sign_up_list":sign_up_list,"revenue_list":revenue_list}
    
    user = {"name":'Admin', "job":'admin','user_id': 'admin'}
    return render_template('admin.html',user = user, all_data = all_data)

@app.route('/show-file/<file_id>')
def show_file(file_id):
    file_temp = fs.find_one({"_id":ObjectId(file_id)})
    if not file_temp:
        return 'No file Content'
    return Response(file_temp.read(), content_type=file_temp.content_type,
                        headers={
                            'Content-Length': file_temp.length
                        })

@app.route('/admin/view-application/<string:teacher_id>', methods=['GET'])
def view_application(teacher_id):
    teacher = db_teachers.find_one({"_id": ObjectId(teacher_id)})
    user_info = {}
    if teacher != None:
        user_info['user_id'] = str(teacher['_id'])
        user_info['First Name'] = teacher['First Name']
        user_info['Last Name'] = teacher['Last Name']
        user_info['balance'] = teacher['balance']
        user_info['Photo'] = teacher['Photo']
        user_info['email'] = teacher['email']
        user_info['Date Of Birth'] = teacher['Date Of Birth']
        id_temp = db.fs.files.find_one({"_id":teacher['Id Document']})
        if len(id_temp['filename']) >0 :
            user_info['Id Document'] = id_temp['filename']
            user_info['Id_id'] = str(id_temp['_id'])
        else:
            user_info['Id Document'] =""
            user_info['Id_id'] =""
        certification_temp = db.fs.files.find_one({"_id":teacher['Certificate Document']})
        if len(id_temp['filename']) >0 :
            user_info['cer_id'] = str(certification_temp['_id'])
            user_info['Certificate Document'] = certification_temp['filename']
        else:
            user_info['cer_id'] = ""
            user_info['Certificate Document'] = "" 
        additional_temp = db.fs.files.find_one({"_id":teacher['Additional Document']})
        if len(id_temp['filename']) >0 :
            user_info['add_id'] = str(additional_temp['_id'])
            user_info['Additional Document'] = additional_temp['filename']
        else:
            user_info['add_id'] = ""
            user_info['Additional Document'] = ""
        user_info['Teaching Levels'] = teacher['Teaching Levels']
        user_info['Subjects'] = teacher['Subjects']
        user_info['Experience'] = teacher['Experience']
        user_info['Graduate'] = teacher['Graduate']
        user_info['Phone Number'] = teacher['Phone Number']
        user_info['mobile_number'] = teacher['mobile_number']
        user_info['time_zone'] = teacher['time_zone']
        user_info['hourly'] = teacher['hourly']
        user_info['Date Signed Up'] = teacher['Date Signed Up']
        user_info['Rating'] = teacher['Rating']
        user_info['Paypal email'] = teacher['Paypal email']
        user_info['Bank detail'] = teacher['Bank detail']
        user_info['teacher_id'] = teacher['teacher_id']
        user_info['approve'] = teacher['approve']
        print(user_info)
    user = {'name': 'Admin', 'user_id': 'admin', 'balance': 0, 'user_info': user_info, 'job': 'admin'}
    return render_template('admin-view-application.html', user=user)


@app.route("/admin/teacher-applications",methods=['GET'])
@alogin_check
def teacher_application():
    applied_cnt = db_teachers.find({}).count()
    rejected_cnt = db_teachers.find({"approve":2}).count()
    accepted_cnt = db_teachers.find({"approve":1}).count()
    pending_cnt = db_teachers.find({"approve":0}).count()
    teachers = db_teachers.find({"approve":0})
    teacher_list = []
    if teachers != None:
        for teacher in teachers:
            temp = {}
            temp['teacher_id'] = str(teacher['_id'])
            temp['full name'] = teacher['First Name'] + " " + teacher['Last Name']
            temp['email'] = teacher['email']
            temp['phone'] = teacher['Phone Number']
            teacher_list.append(temp)
    data = {"applied_cnt":applied_cnt, "rejected_cnt":rejected_cnt, "accepted_cnt":accepted_cnt, "pending_cnt":pending_cnt, "teacher_list":teacher_list}
    user = {"name":'Admin','user_id': 'admin', "job":'admin'}
    return render_template('admin-teacher-application.html',user = user, data = data)

# ajax
@app.route('/admin/set-approve', methods=["POST"])
def set_approve():
    temp = request.form['data']
    temp = json.loads(temp)
    teacher_id = temp['teacher_id']
    teacher_temp = db_teachers.find_one({"_id":ObjectId(teacher_id)})
    if temp['approve'] == "accept":
        teacher_temp['approve'] = 1
        data = {"user": str(teacher_id),
            "is_loggedin": False,
            "is_online": True}
        is_loggedin = db_is_loggedin.insert(data, check_keys=False)
    elif temp['approve'] == 'decline':
        teacher_temp['approve'] = 2
    db_teachers.update({"_id": ObjectId(teacher_id)}, {"$set": teacher_temp})
    # create user in logged in table
    user_info = {}
    user_info['name'] = teacher_temp['First Name']
    user_info['email'] = teacher_temp['email']
    sendemail_accept(user_info)
    msg = {"success": True}
    return jsonify(msg)

@app.route("/admin/allusers",methods=['GET'])
@alogin_check
def all_users():
    teachers = db_teachers.find({"approve":1})
    teachers_list = []
    if teachers != None:
        for itor in teachers:
            temp = {}
            temp['teacher_id'] = str(itor['_id'])
            temp['registration_time'] = itor['Date Signed Up']
            temp['Name'] = itor['First Name'] + " " + itor['Last Name']
            temp['email'] = itor['email']
            temp['Balance'] = round(itor['balance'], 2)
            temp['phone'] = itor['Phone Number']
            teachers_list.append(temp)
    students = db_students.find({})
    student_list = []            
    if students != None:
        for itor in students:
            temp = {}
            temp['student_id'] = str(itor['_id'])
            temp['registration_time'] = itor['Date Signed Up']
            temp['Name'] = itor['First Name'] + " " + itor['Last Name']
            temp['email'] = itor['email']
            temp['phone'] = itor['Phone Number']
            temp['Balance'] = round(itor['Balance'], 2)
            student_list.append(temp)
    data = {'Students':student_list, "Teachers": teachers_list}
    user = {"name":'Admin','user_id': 'admin', "job":'admin'}
    return render_template('admin-allusers.html',user = user, data = data)


@app.route("/admin/financial",methods=['GET'])
@alogin_check
def adminfinancial():
    agr = [ {'$group': {'_id': 'null', 'balance': { '$sum': '$Price paid' } } } ]
    temp_sessions = list(db_sessions.aggregate(agr))
    total_revenue = 0
    if len(temp_sessions) > 0 :
        total_revenue = round((temp_sessions[0]['balance']*0.2)/1.1, 2)
    total_pending_withdraw = db_withdraws.find({'status':0}).count()
    total_paid_to_teachers = 0
    total_in_student_waller = 0
    total_in_teacher_waller = 0
    agr = [ {'$group': {'_id': 'null', 'balance': { '$sum': '$amount' } } } ]
    temp_sessions = list(db_withdraws.aggregate(agr))
    if len(temp_sessions) > 0:
        total_paid_to_teachers = round(temp_sessions[0]['balance'], 2)
        
    agr = [ {'$group': {'_id': 'null', 'balance': { '$sum': '$Balance' } } } ]
    temp_sessions = list(db_students.aggregate(agr))
    if len(temp_sessions) > 0:
        total_in_student_waller = round(temp_sessions[0]['balance'] , 2)
    agr = [ {'$group': {'_id': 'null', 'balance': { '$sum': '$balance' } } } ]
    temp_sessions = list(db_teachers.aggregate(agr))
    if len(temp_sessions) > 0:
        total_in_teacher_waller = round(temp_sessions[0]['balance'], 2)
    transation_temp = db_transactions.find({}).sort('tran_time',pymongo.DESCENDING)
    transaion_list = []
    if transation_temp != None:
        for item in transation_temp:
            temp = {}
            temp['transaction_id'] = str(item['_id'])
            temp['date'] = item['tran_time']
            student_temp = db_students.find_one({"_id":ObjectId(item['user_id'])})
            temp['student_name'] = student_temp['First Name'] + " " + student_temp['Last Name']
            temp['student_id'] = item['user_id']
            temp['amount'] = item['funded_amount']
            temp['invoice'] = item['invoice_number']
            temp['new_balance'] = item['new_balance']
            transaion_list.append(temp)
    withdraw_temp = db_withdraws.find({"status":0}).sort('tran_time',pymongo.ASCENDING)
    pending_withdraw_list = []
    if withdraw_temp != None:
        for item in withdraw_temp:
            temp = {}
            temp['date'] = item['request_date']
            teacher_temp = db_teachers.find_one({'_id':ObjectId(item['user_id'])})
            temp['teacher_name'] = teacher_temp['First Name'] + " " + teacher_temp['Last Name']
            temp['teacher_id'] = item['user_id']
            temp['amount'] = item['amount']
            temp['withdraw_request'] = item['request number']
            pending_withdraw_list.append(temp)
    withdraw_temp = db_withdraws.find({"status":1}).sort('tran_time',pymongo.DESCENDING)
    withdraw_list = []
    if withdraw_temp != None:
        for item in withdraw_temp:
            temp = {}
            temp['date'] = item['complete_date']
            teacher_temp = db_teachers.find_one({'_id':ObjectId(item['user_id'])})
            temp['teacher_name'] = teacher_temp['First Name'] + " " + teacher_temp['Last Name']
            temp['teacher_id'] = item['user_id']
            temp['amount'] = item['amount']
            temp['withdraw_request'] = item['request number']
            withdraw_list.append(temp)
    all_info = {'t_revenue':total_revenue, 't_pending_withdraw': total_pending_withdraw, 't_paid_to_teach': total_paid_to_teachers,
                't_student_w':total_in_student_waller, 't_teacher_w':total_in_teacher_waller, 'tran_list':transaion_list, 
                "pending_w":pending_withdraw_list, 'withdraw_list':withdraw_list}
    user = {"name":'Admin','user_id': 'admin', "job":'admin'}
    return render_template('admin-financial.html',user = user, all_info = all_info)

@app.route('/admin/teacher-profile/<string:user_id>', methods=['GET'])
def admin_teacher_profile(user_id):
    teacher = db_teachers.find_one({"_id": ObjectId(user_id)})
    user = {'name': 'Admin', 'user_id': user_id, 'balance': teacher['balance'],'user_info':teacher,'job':'admin'}
    return render_template('teacher-profile.html', user=user)

@app.route('/admin/student-profile/<string:user_id>', methods=['GET'])
def admin_student_profile(user_id):
    student = db_students.find_one({"_id": ObjectId(user_id)})
    user = {'name': 'Admin', 'user_id': user_id, 'balance': round(student['Balance'], 2),'user_info':student, 'job': 'admin'}
    return render_template('student-profile.html', user=user)

@app.route("/admin/withdraw/<string:id>" , methods=['GET'])
@alogin_check
def withdrawPage(id):
    withdraw_temp = db_withdraws.find_one({'request number': id})
    withdraw_info = {}
    prev_session = []
    if withdraw_temp != None:
        withdraw_info['id'] = id
        withdraw_info['amount'] = withdraw_temp['amount']
        teacher_temp = db_teachers.find_one({'_id':ObjectId(withdraw_temp['user_id'])})
        withdraw_info['teacher_name'] = teacher_temp['First Name'] + " " + teacher_temp['Last Name']
        withdraw_info['teacher_email'] = teacher_temp['email']
        withdraw_info['phone_number'] = teacher_temp['Phone Number']
        withdraw_info['paymentmethod'] = withdraw_temp['payment method']
        withdraw_info['paypal_address'] = teacher_temp['Paypal email']
        withdraw_info['bank_detail'] = teacher_temp['Bank detail']
        session_temp = db_sessions.find({'teacher_id':str(teacher_temp['_id'])})
        for item in session_temp:
            temp = {}
            temp['date'] = item['Start Time']
            temp['session_id'] = str(item['_id'])
            student_temp = db_students.find_one({"_id":ObjectId(item['student_id'])})
            temp['student_name'] = student_temp['First Name'] + " " + student_temp['Last Name']
            temp['student_id'] = str(student_temp['_id'])
            temp['Duration'] = round(item['Duration'], 2)
            temp['balance'] = round(item['Price paid'], 2)
            temp['Rating'] = item['Teacher Rating']
            prev_session.append(temp)
    withdraw_info['pre_session'] = prev_session
    user = {"name":'Admin','user_id': 'admin', "job":'admin'}
    return render_template('admin-withdraw.html',user = user, withdraw_info = withdraw_info)

def withdraw_paypal(email, amount, currency):
    sender_batch_id = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": sender_batch_id,
            "email_subject": "You have a payment"
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": amount,
                    "currency": currency
                },
                "receiver": email,
                "note": "Thank you.",
                "sender_item_id": "item_1"
            }
        ]
    })
    if payout.create(sync_mode=False):
        print("payout[%s] created successfully" % (payout.batch_header.payout_batch_id))
        print(payout)
    else:
        print(payout.error)
        return False
    return True

# ajax
@app.route('/admin/withdraw-complete/<string:id>' , methods=["POST"])
def withdraw_complete(id):
    resp = {'success': True, 'msg': ''}
    withdraw_temp = db_withdraws.find_one({'request number': id})
    if withdraw_temp != None:
        if withdraw_temp['status'] == 1:
             resp['success'] = False
             resp['msg'] = 'Already completed.'
             return jsonify(resp)
        pay_method = withdraw_temp['payment method']
        bpaid = 0
        user_id = withdraw_temp['user_id']
        amount = withdraw_temp['amount']
        teacher = db_teachers.find_one({'_id': ObjectId(user_id)})
        if pay_method == 'paypal':
            resp['success'] = True
            bpaid = 1
            '''
            if teacher == None or teacher['Paypal email'] == '':
                resp['msg'] = 'No Paypal email data.'
                resp['success'] = False
            else:
                email = teacher['Paypal email']
                usd_amount = round(amount / 3.673, 2)
                if withdraw_paypal(email, usd_amount, 'USD'):
                    bpaid = 1
                else:
                    resp['msg'] = 'Error while creating payout.'
                    resp['success'] = False
            '''
        else:
            resp['success'] = True
            bpaid = 1
        if bpaid == 1:
            withdraw_temp['status'] = 1
            withdraw_temp['complete_date'] = datetime.now()
            db_withdraws.update({'request number': id}, {"$set": withdraw_temp})
            b = teacher['balance'] - amount 
            teacher['balance'] = round(b, 2)
            db_teachers.update({'_id': ObjectId(user_id)}, {"$set": teacher})
    else:
        resp['success'] = False
        resp['msg'] = "No pending withdraw entity"
    return jsonify(resp)

# ajax
@app.route('/admin/withdraw-decline/<string:id>' , methods=["POST"])
def withdraw_decline(id):
    resp = {'success': True, 'msg': ''}
    withdraw_temp = db_withdraws.find_one({'request number': id})
    if withdraw_temp != None:
        if withdraw_temp['status'] == 1:
             resp['success'] = False
             resp['msg'] = "Already completed. You can't decline."
        else:
            db_withdraws.delete_one({'request number': id})
    else:
        resp['success'] = False
        resp['msg'] = "Already declined."
    return jsonify(resp)

@app.route('/amdin/session-page/<string:session_id>', methods = ["GET"])
@alogin_check
def session_info(session_id):
    session_temp = db_sessions.find_one({"_id":ObjectId(session_id)})
    info_session = []
    info_session['date'] = datetime.strptime(session_temp['Start Time'], '%d/%m/%Y, %H:%M:%S')
    info_session['Hours'] = round(session_temp['Duration'], 2)
    info_session['Price'] = round(session_temp['Price paid'],2)
    info_session['sessionID'] = str(session_temp['_id'])
    question_temp = db_questions.find_one({"id":ObjectId(session_temp['question id'])})
    info_session['subject'] = question_temp['subject']
    student = db_students.find_one({"_id":ObjectId(session_temp['student_id'])})
    info_session['student name'] = student['First Name'] + " " + student['Last Name']
    teacher = db_teachers.find_one({"_id":ObjectId(session_temp['teacher_id'])})
    info_session['teacher name'] = teacher['First Name'] + " " + teacher['Last Name']
    info_session['Question'] = question_temp['question']
    info_session['pictures'] = question_temp['images']
    info_session['video_link'] = session_temp['recording_url']
    info_session['download_file'] = session_temp['video']
    user = {"name":'Admin','user_id': 'admin', "job":'admin'}
    return render_template("admin-sessionPage.html", user = user , info = info_session)

@app.route("/admin/live-sessions",methods=['GET'])
@alogin_check
def live_sessions():
    questions = db_questions.find({'$or': [{"status": 0}, {"status": 1}, {"status": 2}]})
    pending_qus = []
    cnt_qus = 0
    if questions != None:
        for item in questions:
            cnt_qus += 1
            temp = {}
            student_temp = db_students.find_one({"_id":ObjectId(item['user_id'])})
            if student_temp == None:
                continue
            temp['question_id'] = str(item['_id'])
            temp['date'] = datetime.fromtimestamp(int(item['Date of Question']))
            temp['Student Name'] = student_temp['First Name'] + " " + student_temp['Last Name']
            temp['student_id'] = str(student_temp['_id'])
            temp['Subject'] = item['subject']
            temp['Question'] = item['question']
            temp["Pictures"] = item["images"]
            pending_qus.append(temp)
    teachers = db_is_loggedin.find({})
    cnt_teach = 0
    if teachers != None:
        for itor in teachers:
            if 'is_online' not in itor:
                continue
            if itor['is_online'] == True:
                cnt_teach +=1
    session_db = db_sessions.find({"status":{'$lt': 2}}).sort('Start Time',pymongo.DESCENDING)
    cnt_ses = session_db.count()
    session_list = []
    if session_db != None:
        for item in session_db:
            temp = {}
            temp['session ID'] = str(item['_id'])
            student_temp = db_students.find_one({"_id":ObjectId(item['student_id'])})
            teacher_temp = db_teachers.find_one({"_id":ObjectId(item['teacher_id'])})
            question_temp = db_questions.find_one({"_id":ObjectId(item['question id'])})
            if student_temp == None or teacher_temp == None:
                continue
            temp['Student Name'] = student_temp['First Name'] + " " + student_temp['Last Name']
            temp['student_id'] = str(student_temp['_id'])
            temp['Teacher Name'] = teacher_temp['First Name'] + " " + teacher_temp['Last Name']
            temp['teacher_id'] = str(teacher_temp['_id'])
            temp['Subject'] = question_temp['subject']
            temp['date'] = datetime.strptime(item['Start Time'], '%d/%m/%Y, %H:%M:%S')
            session_list.append(temp)
    data = {"num_pend_qus":cnt_qus, "num_of_teach": cnt_teach, "num_of_sess": cnt_ses , "LiveSession":session_list, "PendQuestion":pending_qus}
    user = {"name":'Admin','user_id': 'admin', "job":'admin'}
    return render_template('admin-live-sessions.html', user = user, data = data)

# ajax
@app.route('/admin/cancel_question/<string:question_id>' , methods=["POST"])
def cancel_question(question_id):
    question_temp = db_questions.find_one({"_id":ObjectId(question_id)})
    if int(question_temp['status']) < 2:
        db_questions.delete_one({"_id":ObjectId(question_id)})
    else:
        db_questions.delete_one({"_id":ObjectId(question_id)})
        session_temp = db_sessions.find_one({"question id":question_id})
        db_sessions.delete_one({"question id":question_id})
        class_id = session_temp['class_id']
        params = {'method':'Cancel',
				'class_id':class_id
				}
        with open(class_id + ".json", 'w') as json_file:
            json.dump(params, json_file)
        os.system('ruby WiZiQServices.rb ' + class_id + ".json")
        os.remove(class_id + ".json")
    msg = {"success": True}
    return jsonify(msg)

@app.route("/admin/sessions-history",methods=['GET'])
@alogin_check
def sessions_his():
    sessions_temp = db_sessions.find({'status': { '$in': [2, 4] }}).sort('Start Time',pymongo.DESCENDING)
    cnt = sessions_temp.count()
    session_list = []
    total_hours = 0
    if sessions_temp != None:
        for item in sessions_temp:
            temp = {}
            temp['date'] = datetime.strptime(item['Start Time'], '%d/%m/%Y, %H:%M:%S')
            temp["session_ID"] = str(item['_id'])
            question_temp = db_questions.find_one({"_id":ObjectId(item['question id'])})
            temp['Subject'] = question_temp['subject']
            time_temp = round(item['Duration'], 2)
            mins = str(int(time_temp))
            str_temp = mins.zfill(2) + ":"
            time_temp -= int(time_temp)
            secs = str(int(time_temp * 60))
            str_temp += secs.zfill(2)
            temp['length'] = str_temp
            total_hours += item['Duration']
            temp['total_paid'] = item['Price paid']
            temp['rating'] = item['Teacher Rating']
            session_list.append(temp)
    session_history = {}
    session_history['session_cnt'] = cnt
    session_history['total_hours'] = round(total_hours/60,2)
    session_history['session_list'] = session_list
    user = {"name":'Admin','user_id': 'admin', "job":'admin'}
    return render_template('admin-sessions-history.html', user = user ,session_history = session_history)

@app.route("/admin/flags",methods=['GET'])
@alogin_check
def admin_flags():
    #flg_session = db_sessions.find({"$or":[{"Student Rating":{ '$gte':0, '$lt':4}} , {"Teacher Rating":{ '$gte':0, '$lt':4}}]}).sort('Start Time',pymongo.DESCENDING)
    flg_session = db_sessions.find({'status':4}).sort('Start Time',pymongo.DESCENDING)
    flg_list = []
    if flg_session != None:
        for item in flg_session:
            temp = {}
            temp['date'] = item['Start Time']
            temp['Session_ID'] = str(item['_id'])
            temp['Amount'] = item['Price paid']
            teacher = db_teachers.find_one({"_id":ObjectId(item['teacher_id'])})
            temp['username'] = teacher['First Name'] + " " + teacher['Last Name']
            temp['user_id'] = str(teacher['_id'])
            temp['job'] = 'teacher'
            temp['Rating'] = item['Teacher Rating']
            flg_list.append(temp)
    user = {'name':'Admin','user_id': 'admin', "job": 'admin'}
    return render_template('admin-flags.html',user = user, flg_list = flg_list)

@app.route('/admin/teacher-info/<string:teacher_id>', methods=["GET"])
@alogin_check
def teacher_Info(teacher_id):
    teacher = db_teachers.find_one({"_id":ObjectId(teacher_id)})
    info = {}
    info['Name'] = teacher['First Name'] + " " + teacher["Last Name"]
    info['teacher id'] = teacher_id
    info['email'] = teacher['email']
    info['phone number'] = teacher['Phone Number']
    session_temp = db_sessions.find({"teacher_id":teacher_id}).sort('Start Time',pymongo.DESCENDING)
    info['total_sessions'] = session_temp.count()
    info['cur_balance'] = teacher['balance']
    total_earned = 0
    session_list = []
    if session_temp != None:
        for item in session_temp:
            temp = {}
            temp['date'] = item['Start Time']
            temp['Session_ID'] = str(item['_id'])
            temp['Amount'] = item['Price paid']
            total_earned += item['Price paid']
            student_temp = db_students.find_one({"_id":ObjectId(item['student_id'])})
            temp['Student Name'] = student_temp['First Name'] + " " + student_temp['Last Name']
            temp['student_id'] = str(student_temp['_id'])
            time_temp = round(item['Duration'], 2)
            mins = str(int(time_temp))
            str_temp = mins.zfill(2) + ":"
            time_temp -= int(time_temp)
            secs = str(int(time_temp * 60))
            str_temp += secs.zfill(2)
            temp['Duration'] = str_temp
            temp['amount'] = item['Price paid']
            temp['rating'] = item['Teacher Rating']
            session_list.append(temp)
    info['session_list'] = session_list
    info['total_earned'] = round(total_earned * 0.9, 2)
    paymet_detail = {}
    paymet_detail['paypal_email'] = teacher['Paypal email']
    paymet_detail['bank_detail'] = teacher['Bank detail']
    info['payment_detail'] = paymet_detail
    user = {'name':'Admin','user_id': 'admin', "job": 'admin'}
    return render_template("admin-teacher-info.html", user = user, info = info)

# ajax
@app.route('/admin/remove-one/<string:user_id>',methods=["POST"])
def remove_one(user_id):
    temp = request.form['data']
    temp = json.loads(temp)
    job = temp['job']
    if job =='teacher':
        teacher_temp = db_teachers.find_one({"_id":ObjectId(user_id)})
        if teacher_temp != None:
            teacher_temp['approve'] = 3
            db_teachers.update({"_id": ObjectId(user_id)}, {"$set": teacher_temp})
            db_is_loggedin.delete_one({'user':user_id})
        else:
            msg = {"success": False}
            return jsonify(msg)
    elif job == 'student':
        student_all = db_students.find({})
        if student_all != None:
            for item in student_all:
                item['status'] = 0
                db_students.update({"_id":item['_id']}, {"$set":item})
        student_temp = db_students.find_one({'_id':ObjectId(user_id)})
        if student_temp != None:
            student_temp['status'] = 3
            db_students.update({"_id":ObjectId(user_id)}, {"$set":student_temp})
            db_is_loggedin.delete_one({"user":user_id})
    msg = {"success": True}
    return jsonify(msg)

# ajax
@app.route("/admin/balance-manage/<string:user_id>", methods=['POST'])
def balance_manage(user_id):
    temp = request.form['data']
    temp = json.loads(temp)
    manageMethod = temp['manageMethod']
    job = temp['job']
    if job == 'student':
        student_temp = db_students.find_one({"_id":ObjectId(user_id)})
        if manageMethod == 'addBalance':
            student_temp['Balance'] += int(temp['amount'])
        elif manageMethod == 'removeBalance':
            if student_temp['Balance'] - int(temp['amount']) < 0 :
                msg = {"success": False, "msg": "Balance can be negative value."}
                return jsonify(msg)
            student_temp['Balance'] -= int(temp['amount'])
        db_students.update({"_id": ObjectId(user_id)}, {"$set": student_temp})
        msg = {"success": True}
        return jsonify(msg)
    elif job == 'teacher':
        teacher_temp = db_teachers.find_one({"_id":ObjectId(user_id)})
        if manageMethod == 'addBalance':
            teacher_temp['balance'] += int(temp['amount'])
        elif manageMethod == 'removeBalance':
            if teacher_temp['balance'] - int(temp['amount']) < 0 :
                msg = {"success": False, "msg": "Balance can be negative value."}
                return jsonify(msg)
            teacher_temp['balance'] -= int(temp['amount'])
        db_teachers.update({"_id": ObjectId(user_id)}, {"$set": teacher_temp})
        msg = {"success": True}
        return jsonify(msg)

@app.route('/admin/student-info/<string:student_id>', methods=["GET"])
@alogin_check
def student_Info(student_id):
    student = db_students.find_one({"_id":ObjectId(student_id)})
    info = {}
    info['Name'] = student['First Name'] + " " + student["Last Name"]
    info['student id'] = student_id
    info['email'] = student['email']
    info['phone number'] = student['Phone Number']
    session_temp = db_sessions.find({"student_id":student_id}).sort('Start Time',pymongo.DESCENDING)
    info['total_sessions'] = session_temp.count()
    info['cur_balance'] = round(student['Balance'], 2)
    total_earned = 0
    session_list = []
    for item in session_temp:
        temp = {}
        temp['date'] = item['Start Time']
        temp['Session_ID'] = str(item['_id'])
        temp['Amount'] = item['Price paid']
        total_earned += item['Price paid']
        teacher_temp = db_teachers.find_one({"_id":ObjectId(item['teacher_id'])})
        if teacher_temp == None:
            continue
        temp['Teacher Name'] = teacher_temp['First Name'] + " " + teacher_temp['Last Name']
        temp['teacher_id'] = str(teacher_temp['_id'])
        time_temp = round(item['Duration'], 2)
        mins = str(int(time_temp))
        str_temp = mins.zfill(2) + ":"
        time_temp -= int(time_temp)
        secs = str(int(time_temp * 60))
        str_temp += secs.zfill(2)
        temp['Duration'] = str_temp
        temp['amount'] = item['Price paid']
        temp['rating'] = item['Student Rating']
        session_list.append(temp)
    info['session_list'] = session_list
    info['total_paid'] = total_earned
    user = {'name':'Admin','user_id': 'admin', "job": 'admin'}
    return render_template("admin-student-info.html", user = user, info = info)
    
@app.route('/teacher', methods=['GET'])
@tlogin_check
def teacher_dashboard():
    user_id = session['user_id']
    teacher = db_teachers.find_one({"_id": ObjectId(user_id)})
    session_temp = db_sessions.find({"teacher_id":user_id}).sort('Start Time',pymongo.DESCENDING)
    total_sessions = 0
    total_hours = 0
    total_earned = round(teacher['balance'],2)
    session_info = []
    temp ={}
    if session_temp != None:
        for item in session_temp:
            total_sessions +=1
            temp = {}
            time1 = datetime.strptime(item['Start Time'], '%d/%m/%Y, %H:%M:%S').date().strftime("%d/%m/%Y")
            #time1 = "2010-2-2"
            temp['date'] = time1
            temp['session_id'] = str(item['_id'])
            time_temp = round(item['Duration'], 2)
            mins = str(int(time_temp))
            str_temp = mins.zfill(2) + ":"
            time_temp -= int(time_temp)
            secs = str(int(time_temp * 60))
            str_temp += secs.zfill(2)
            temp['length'] = str_temp
            total_hours += round(item['Duration'],2)
            question = db_questions.find_one({'_id':ObjectId(item['question id'])})
            temp['Subject'] = question['subject']
            temp['Text'] = question['question']
            temp['Price Paid'] = item['Price paid']
            session_info.append(temp)
    avg_session_len = 0
    if total_sessions > 0:
        avg_session_len = total_hours/total_sessions
    user = {'name': teacher['First Name'], 'user_id': user_id, 'is_online':session['is_online'],'balance':round(teacher['balance'], 2),'job':session['job'],
             'subjects': teacher['Subjects'],'total_hours':round(total_hours/60,2),'total_sessions':total_sessions,'job':'teacher',
             'avg_sessions':round(avg_session_len, 2),'total_earned':round(total_earned, 2),'sessions':session_info}
    return render_template('teacher-dashboard.html', user=user)

# ajax
@app.route('/teacher/status', methods=['POST'])
def set_online_status():
    temp = request.form['data']
    temp = json.loads(temp)
    is_online = temp['online_state']
    user_id = session['user_id']
    session['is_online'] = is_online
    is_online_db = db_is_loggedin.find_one({"user": str(user_id)})
    is_online_db['is_online'] = is_online
    db_is_loggedin.update({"user": str(user_id)}, {"$set": is_online_db})
    msg = {"success": True}
    return jsonify(msg)

@app.route('/teacher/financial', methods=['GET'])
@tlogin_check
def financial():
    user_id = session['user_id']
    user1 = db_teachers.find_one({"_id": ObjectId(user_id)})
    user = {}
    user['user_id'] = user_id
    user['name'] = user1['First Name']
    user['balance'] = user1['balance']
    user['Paypal email'] = user1['Paypal email']
    bank_detail = user1['Bank detail']
    session1 = db_sessions.find({"teacher_id": user_id}).sort('Start Time',pymongo.DESCENDING)
    session2 = []
    if session1 != None:
        for item in session1:
            tem_session = {}
            tem_session['date'] = item['Start Time']
            tem_session['session_id'] = str(item['_id'])
            time_temp = round(item['Duration'], 2)
            mins = str(int(time_temp))
            str_temp = mins.zfill(2) + ":"
            time_temp -= int(time_temp)
            secs = str(int(time_temp * 60))
            str_temp += secs.zfill(2)
            tem_session['length'] = str_temp
            tem_session['new_balance'] = round(item['new_balance'],2)
            tem_session['earned_money'] = round((item['Price paid']*0.9), 2)
            session2.append(tem_session)
    user['session'] = session2
    user['job'] = 'teacher'
    return render_template('financial.html', user=user, bank_detail=bank_detail)

@app.route('/teacher/withdraw', methods=['POST'])
def teacher_withdraw():
    temp = request.form['data']
    temp = json.loads(temp)
    paymethod = temp['paymentMethod']
    withdraw_temp = db_withdraws.find({"user_id":str(session['user_id'])})
    amt = 0
    if withdraw_temp != None:
        for item in withdraw_temp:
            if item['status'] != 0:
                continue
            amt += item['amount']
    teacher_temp = db_teachers.find_one({"_id": ObjectId(session['user_id'])})
    resp={}
    
    if amt +  round(float(temp['withdrawamount']),2) > teacher_temp['balance']:
        resp['success'] = False
        resp['msg'] = "You have already pending withdraw request."
        return jsonify(resp)
    withdraw_temp = {}
    withdraw_temp['user_id'] = str(session['user_id'])
    withdraw_temp['amount'] = round(float(temp['withdrawamount']),2)
    withdraw_temp['request_date'] = datetime.now()
    cnt = 1
    if db_withdraws.find({}).count() > 0:
        withdraw_db = db_withdraws.find().sort("_id",-1).limit(1)
        if withdraw_db != None:
            cnt = int(withdraw_db[0]['request number']) + 1
    tmp = str(cnt)
    withdraw_temp['request number'] = tmp.zfill(6)
    withdraw_temp['complete_date'] = ""
    withdraw_temp['payment method'] = paymethod
    withdraw_temp['status'] = 0
    db_withdraws.insert(withdraw_temp, check_keys=False)
    resp = {"success": True,"msg": "Withdraw is pending now."}
    return jsonify(resp)
    
@app.route('/teacher/profile/<string:user_id>', methods=['GET'])
def teacher_profile(user_id):
    teacher = db_teachers.find_one({"_id": ObjectId(user_id)})
    user = {'name': teacher['First Name'], 'user_id': user_id, 'balance': teacher['balance'],'user_info':teacher,'job':'teacher'}
    return render_template('teacher-profile.html', user=user)

# ajax
@app.route('/teacher/profile-save',methods=['POST'])
def profile_save():
    temp = request.form['data']
    temp = json.loads(temp)
    phone = temp['Phone Number']
    print("---------------phone number-------------")
    try:
        z = phonenumbers.parse(phone, None)
        b = phonenumbers.is_valid_number(z)
        print(b)
        if b == False:
            resp = {'success': False, 'msg': 'Invalid phone number.'}
            return jsonify(resp)
    except phonenumbers.NumberParseException as e:
        print(e)
        resp = {'success': False, 'msg': 'Invalid phone number.'}
        return jsonify(resp)
    except:
        print("Unexpected error")
        resp = {'success': False, 'msg': 'Invalid phone number.'}
        return jsonify(resp)
    

    user_id = temp['user_id']
    teacher = db_teachers.find_one({"_id":ObjectId(user_id)})
    teacher['First Name'] = temp['First Name']
    teacher['Last Name'] = temp['Last Name']
    #teacher['Date Of Birth'] = temp['Date Of Birth']
    teacher['email'] = temp['email']
    teacher['Phone Number'] = temp['Phone Number']
    
    #teacher['Telegram User Name'] = temp['Telegram User Name']
    #teacher['Teaching Levels'] = temp['Teaching Levels']
    rate = float(temp['rate'])
    rate = round(rate, 2)
    teacher['hourly'] = rate
    db_teachers.update({"_id": ObjectId(user_id)}, {"$set": teacher})
    msg = {"success": True}
    return jsonify(msg)

# ajax
@app.route('/resetpassword' , methods=["POST"])
def resetpassword():
    resp = {"success": True, 'msg': ''}
    temp = request.form['data']
    temp = json.loads(temp)
    user_id = temp['user_id']
    user_job = temp['job']
    pwd = temp['data']
    if user_job == 'student':
        someone = db_students.find_one({'_id': ObjectId(user_id)})
    else:
        someone = db_teachers.find_one({'_id': ObjectId(user_id)})
    if someone == None:
        resp['success'] = False
        resp['msg'] = 'No ' + user_job
        return jsonify(resp)
    db_pwd = someone['password']
    old_pwd = pwd[0]
    new_pwd = pwd[1]
    if not pwd_context.verify(old_pwd, db_pwd):
        resp['success'] = False
        resp['msg'] = 'Old password not correct'
        return jsonify(resp)
    hashed_pwd = pwd_context.hash(new_pwd)
    someone['password'] = hashed_pwd
    if user_job == 'student':
        db_students.update({"_id":ObjectId(user_id)}, {"$set": someone})
    else:
        db_teachers.update({"_id":ObjectId(user_id)}, {"$set": someone})
    return jsonify(resp)

# ajax
@app.route('/teacher/bankdetail-save' , methods=["POST"])
def bank_detail_save():
    temp = request.form['data']
    temp = json.loads(temp)
    data = {'Bank detail': {}}
    data['Bank detail']['receipient name'] = temp['recipientname']
    data['Bank detail']['receipient address'] = temp['recipientaddress']
    data['Bank detail']['bank name'] = temp['bankname']
    data['Bank detail']['routing number'] = temp['abaroutingnum']
    data['Bank detail']['account number'] = temp['recipientbanknumber']
    data['Bank detail']['IBAN'] = temp['ibanumber']
    db_teachers.update({"_id":ObjectId(session['user_id'])}, {"$set": data})
    msg = {"success": True}
    return jsonify(msg)

# ajax
@app.route('/teacher/paypal-save' , methods=["POST"])
def teacher_paypal_save():
    temp = request.form['data']
    temp = json.loads(temp)
    data = {'Paypal email': temp['paypalemail']}
    db_teachers.update({"_id":ObjectId(session['user_id'])}, {"$set": data})
    msg = {"success": True}
    return jsonify(msg)

# ajax
@app.route('/teacher/receive-question', methods=["POST"])
def receive_question():
    resp = {"success": True}
    user_id = session['user_id']
    status = 0
    accepted_question = db_questions.find_one({"accepted_teacher": user_id, '$or': [{"status": 2}, {"status": 3}]})
    make_question = []
    if accepted_question != None:
        status = accepted_question['status']  # 3:live   2: accepted
        if status == 2:
            # -----------------------get session data from session collection-------------------------
            session1 = db_sessions.find_one({'question id': str(accepted_question['_id'])})
            if session1 != None:
                resp['class_id'] = session1['class_id']
                resp['presenter_url'] = session1['presenter_url']
            else:
                resp['class_id'] = ''
                resp['presenter_url'] = ''
    else:
        questions = db_questions.find({"teachers.teacher_id": user_id, "status": {'$lte': 2}})
        for question in questions:
            declined = 0
            accepted = 0
            for item in question['teachers']:
                if item['teacher_id'] != user_id:
                    continue
                if item['accept'] >= 2:
                    declined = 1
                    break
                if item['accept'] == 1:
                    accepted = 1  # you accepted now and counting
                    break
            if declined == 1:
                continue
            if accepted == 1:
                resp['question_id'] = str(question['_id'])  # if counting, no need to get questions
                status = 1
                break
            temp = {}
            temp['question_id'] = str(question['_id'])
            temp['question'] = question['question']
            temp['images'] = question['images']
            temp['student_id'] = str(question['user_id'])
            student_temp = db_students.find_one({"_id": ObjectId(question['user_id'])})
            temp['student'] = student_temp['First Name'] + " " + student_temp['Last Name']
            make_question.append(temp)
    resp['make_question'] = make_question
    resp['status'] = status
    return jsonify(resp)

# ajax
@app.route('/teacher/timeover', methods=['POST'])
def teacher_timeover():
    temp = request.form['data']
    temp = json.loads(temp)
    question_id = str(temp['question_id'])
    t_id = str(temp['teacher_id'])
    question = db_questions.find_one({'_id': ObjectId(question_id)})
    for item in question['teachers']:
        if item['teacher_id'] == t_id:
            item['accept'] = 0
            break
    db_questions.update_one({'_id': ObjectId(question_id)}, {"$set": question}, upsert=False)
    msg = {"success": True}
    return jsonify(msg)

# ajax
@app.route('/teacher/accept', methods=['POST'])
def teacher_accept():
    temp = request.form['data']
    temp = json.loads(temp)
    question_id = str(temp['question_id'])
    statu = str(temp['status'])
    question = db_questions.find_one({'_id': ObjectId(question_id)})
    user_id = session['user_id']
    for item in question['teachers']:
        if item['teacher_id'] == user_id:
            if statu == 'accept':
                item['accept'] = 1
                question['status'] = 1
            else:
                item['accept'] = 2
            break
    db_questions.update_one({'_id': ObjectId(question_id)}, {"$set": question}, upsert=False)
    msg = {"success": True}
    return jsonify(msg)


@app.route('/student', methods=['GET'])
@slogin_check
def student_dashboard():
    user_id = session['user_id']
    pending_question = db_questions.find_one({'user_id':user_id, 'status': {'$lt': 4}})
    if pending_question != None:
        return redirect(url_for('find_teacher', question_id = str(pending_question['_id'])))

    student = db_students.find_one({"_id": ObjectId(user_id)})
    session_temp = db_sessions.find({"student_id":user_id}).sort('Start Time',pymongo.DESCENDING)
    session_info = []
    temp ={}
    if session_temp != None:
        for item in session_temp:
            temp = {}
            time1 = datetime.strptime(item['Start Time'], '%d/%m/%Y, %H:%M:%S')
            temp['date'] = time1
            temp['session_id'] = str(item['_id'])
            time_temp = round(item['Duration'], 2)
            mins = str(int(time_temp))
            str_temp = mins.zfill(2) + ":"
            time_temp -= int(time_temp)
            secs = str(int(time_temp * 60))
            str_temp += secs.zfill(2)
            temp['length'] = str_temp
            question = db_questions.find_one({'_id':ObjectId(item['question id'])})
            temp['Subject'] = question['subject']
            temp['Text'] = question['question']
            temp['Price Paid'] = round(item['Price paid'],2)
            session_info.append(temp)
    user = {'name': student['First Name'], 'user_id': user_id,'sessions':session_info,'balance':round(student['Balance'],2),'job':'student'}
    return render_template('student-dashboard.html', user=user, question='')

# ajax
@app.route("/student/payment", methods=['POST'])
def student_payment():
    amount = request.form['amount']
    amount = round(float(amount) / 3.673, 2)
    return_url = request.form['return_url']
    cancel_url = request.form['cancel_url']
    print("------------------ payment ------------------------")
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Add Funds",
                    "sku": "class",
                    "price": amount,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": amount,
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})             
    if payment.create():
        print("payment success")
        session['fund_amount'] = amount
    else:
        print(payment.error)
    return jsonify({'paymentID': payment.id, 'amount': amount})


# ajax
@app.route("/student/payment_execute", methods=['POST'])
def student_payment_execute():
    resp = {'success': True}
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])
    if payment.execute({'payer_id': request.form['payerID']}):
        print("Execute success")
        user_id = session['user_id']
        amount = float(payment.transactions[0].amount.total)
        fee = float(payment.transactions[0].related_resources[0].sale.transaction_fee.value)
        funded_amount = amount - fee
        amount = round(amount * 3.673, 2)
        fee = round(fee * 3.673, 2)
        funded_amount = round(funded_amount * 3.673, 2)
        transaction = {}
        transaction['user_id'] = user_id
        transaction['payment_method'] = 'paypal'
        transaction['amount'] = amount
        transaction['fee'] = fee
        transaction['funded_amount'] = funded_amount
        transaction['payment_id'] = payment.id
        transaction['payer_id'] = payment.payer.payer_info.payer_id
        transaction['invoice_number'] = payment.id
        transaction['tran_time'] = payment.transactions[0].related_resources[0].sale.create_time
        student = db_students.find_one({"_id": ObjectId(user_id)})
        student['Balance'] += round(funded_amount, 2)
        db_students.update({"_id": ObjectId(user_id)}, {"$set": student})
        transaction['new_balance'] = round(student['Balance'] , 2)
        transaction_id = db_transactions.insert(transaction, check_keys=False)
        print(funded_amount)
        resp['funded_amount'] =  round(funded_amount, 2)
        resp['amount'] = round(amount, 2)
        resp['fee'] = round(fee, 2)
    else:
        resp['success'] = False
        resp['msg'] = payment.error
        print(payment.error)
    return jsonify(resp)

# ajax
@app.route('/api/sendquestion', methods=['POST'])  # Send Question
def sendquestion():
    if request.method == "POST":
        user_id = session['user_id']
        student = db_students.find_one({'_id': ObjectId(user_id)})
        balance = round(student['Balance'], 2)
        if balance < 30:
            msg = {"success": False, 'msg': "You can't send question because your balance is less than 30 AED."}
            return jsonify(msg)
        question = {}
        res = request.form['data']
        res = json.loads(res)
        question['question'] = res['question']
        question['subject'] = res['subject']
        question['images'] = res['images']
        tem_teachs = db_teachers.find({'Subjects': question['subject']})
        teachers = []
        user_list = []
        for item in tem_teachs:
            if item['approve'] != 1:
                continue
            temp_online = db_is_loggedin.find_one({'user': str(item["_id"])})
            if 'is_online' not in temp_online:
                continue
            if temp_online['is_online'] == False:
                continue
            teacher = {}
            teacher['teacher_id'] = str(item.get("_id"))
            teacher['accept'] = 0
            teachers.append(teacher)

            user_info ={}
            user_info['name'] = item['First Name']
            user_info['email'] = item['email']
            user_info['question'] = question['question']
            user_list.append(user_info)

        sendemail_newquestion(user_list)
        question['teachers'] = teachers
        question['user_id'] = session['user_id']
        question['Date of Question'] = str(int(datetime.now().timestamp()))
        question['status'] = 0
        question['accepted_teacher'] = ""
        question['session'] = "session_infomation"
        question_id = db_questions.insert(question, check_keys=False)
        msg = {"success": True, 'question_id': str(question_id)}
        return jsonify(msg)

@app.route('/review-page', methods=['GET'])
def review_page():
    timetemp1 = datetime.now().timestamp()
    res = request.values
    class_id = str(res['class_id'])
    session_temp = db_sessions.find_one({"class_id":class_id})
    student_temp = {}
    teacher_temp = db_teachers.find_one({"_id":ObjectId(session_temp['teacher_id'])})
    student_temp = db_students.find_one({"_id":ObjectId(session_temp['student_id'])})
    question_temp = db_questions.find_one({"_id":ObjectId(session_temp['question id'])})
    if session_temp['Price paid'] == 0:
        question_temp['status'] = 4
        timetemp = datetime.strptime(session_temp['Start Time'], '%d/%m/%Y, %H:%M:%S').timestamp()
        duration = max((timetemp1 - timetemp)/  60, 15)
        hourly = teacher_temp['hourly']
        val = round(min(round((duration * hourly * 1.1)/60,2), student_temp['Balance']) , 2)
        val1 = round(val*0.9/1.1, 2)
        transaction_temp = {}
        session_temp['Price paid'] = round(val/1.1, 2)
        transaction_temp['user_id'] = str(student_temp['_id'])
        transaction_temp['payment_method'] = 'class'
        transaction_temp['amount'] = -1*val
        transaction_temp['fee'] = 0
        transaction_temp["funded_amount"] = -1*val
        transaction_temp['payment_id'] = class_id
        transaction_temp['payer_id'] = str(student_temp['_id'])
        transaction_temp['invoice_number'] = class_id
        transaction_temp['tran_time'] = datetime.now()
        transaction_temp['new_balance'] = round(student_temp['Balance'] - val, 2)
        db_transactions.insert_one(transaction_temp)
        session_temp['Duration'] = duration
        session_temp['status'] = 2
        teacher_temp['balance'] += val1
        student_temp['Balance'] -= val
        session_temp['new_balance'] = teacher_temp['balance']
        db_sessions.update({"class_id":class_id}, {"$set": session_temp})
        db_teachers.update({"_id":ObjectId(session_temp['teacher_id'])}, {"$set": teacher_temp})
        db_students.update({"_id":ObjectId(session_temp['student_id'])}, {"$set": student_temp})
        db_questions.update({"_id":ObjectId(session_temp['question id'])}, {"$set": question_temp})
        mail_info = {}
        time_temp = round(session_temp['Duration'], 2)
        mins = str(int(time_temp))
        str_temp = mins.zfill(2) + ":"
        time_temp -= int(time_temp)
        secs = str(int(time_temp * 60))
        str_temp += secs.zfill(2)
        mail_info['session_length'] = str_temp + " min"
        mail_info['teacher_rate'] = str(teacher_temp['hourly']) + "AED/ h"
        mail_info['service_charge'] = str(round(session_temp['Price paid']/10, 2))
        mail_info['job'] = 'student'
        mail_info['email'] = student_temp['email']
        mail_info['Total'] = str(round(session_temp['Price paid']*1.1, 2))
        sendemail_invoice(mail_info)
        mail_info['job'] = 'teacher'
        mail_info['email'] = teacher_temp['email']
        mail_info['Total'] = str(round(session_temp['Price paid']*0.9, 2))
        sendemail_invoice(mail_info)
    user = {}
    if 'isattendee' in res:
        user['job'] = 'student'
        session['job'] = 'student'
        session['user_id'] = str(student_temp['_id'])
        session['user_name'] = student_temp['First Name']
        user['user_id'] = str(student_temp['_id'])
    elif 'ispresenter' in res:
        user['job'] = 'teacher'
        session['job'] = 'teacher'
        session['user_id'] = str(teacher_temp['_id'])
        session['user_name'] = teacher_temp['First Name']
        is_login_temp = db_is_loggedin.find_one({"user":str(teacher_temp['_id'])})
        if is_login_temp != None:
            session['is_online'] = is_login_temp['is_online']
        user['user_id'] = str(teacher_temp['_id'])

    user['class_id'] = class_id
    if session['job'] =='teacher':
        teacher = db_teachers.find_one({'_id':ObjectId(session['user_id'])})
        user['name'] = teacher['First Name'] +" " + teacher['Last Name']
        user['balance'] = round(teacher['balance'], 2)
    elif session['job'] == 'student':
        student = db_students.find_one({'_id':ObjectId(session['user_id'])})
        user['name'] = student['First Name'] +" " + student['Last Name']
        user['balance'] = round(student['Balance'], 2)
    return render_template("review-page.html", user = user)

# ajax
@app.route("/review/give-review", methods=["POST"])
def give_review():
    res = request.form['data']
    res = json.loads(res)
    session_temp = db_sessions.find_one({'class_id':res['class_id']})
    if session['job'] == 'teacher':
        session_temp['Student Rating'] = res['ratingValue']
    elif session['job'] == 'student':
        session_temp['Teacher Rating'] = res['ratingValue']
        session_temp['status'] = 4
    db_sessions.update({"class_id":res['class_id']}, {"$set": session_temp})
    rating = db_sessions.aggregate([{ '$match': {"teacher_id": session_temp['teacher_id']}}, {'$group': {'_id': "$teacher_id",'avgrating': { '$avg': "$Teacher Rating" }}}])
    rating = list(rating)
    teacher_temp = db_teachers.find_one({"_id":ObjectId(session_temp['teacher_id'])})
    teacher_temp['Rating'] = round(rating[0]['avgrating'], 2)
    db_teachers.update({"_id":ObjectId(session_temp['teacher_id'])}, {"$set": teacher_temp})
    msg = {"success": True}
    return jsonify(msg)

# ajax
@app.route('/status-ping',methods=['POST'])
def status_ping():
    class_id= str(request.form['class_id'])
    class_status = str(request.form['class_status'])
    recording_status = str(request.form['recording_status'])
    session1 = db_sessions.find_one()
    print("------------------------------------------Test Ping status---------------------------------------")
    print("class id: "+class_id+ "   class status: " + class_status + "   recording_status: " +  recording_status)
    pass

def add_teacher(teacher_id):
    teacher = db_teachers.find_one({"_id": ObjectId(teacher_id)})
    params = {'method': 'add_teacher',
              #'teacher_id': str(teacher['teacher_id']),
              'teacher_id': str(teacher['teacher_id']),
              'name': teacher['First Name'] + " " + teacher['Last Name'],
              'email': teacher['email'],
              'password': 'takweya',
              'image': dir + "/static/photos/" + 'avatar.png',
              'phone_number': teacher['Phone Number'],
              'mobile_number': teacher['mobile_number'],
              'time_zone': teacher['time_zone'],
              'about_the_teacher': teacher['Experience'],
              'can_schedule_class': 0,
              'is_active': 1
              }
    str_filename = str(teacher_id) + '.json'
    with open(str_filename, 'w') as json_file:
        json.dump(params, json_file)
    os.system('ruby WiZiQServices.rb '+ str_filename)
    
def create_class(question, url_temp):
    title = question['subject'] + "Class"
    student = db_students.find_one({"_id":ObjectId(question['user_id'])})
    val = round(student['Balance'], 2)
    teacher = db_teachers.find_one({"_id": ObjectId(question['accepted_teacher'])})
    tim = 0
    if teacher['hourly'] > 0:
        tim = min(math.floor((val*60)/(teacher['hourly'] * 1.1)),270)
    else:
        tim = 1
    tim = max(tim, 15)
    domain='http://'+url_temp.split('//')[-1].split('/')[0]+"/review-page"
    params = {'method': 'create',
              'title': title,
              'language_culture_name':'en-us',
              #'time_zone': teacher['time_zone'],
              'presenter_default_controls': 'audio, video',
              'attendee_default_controls': 'audio',
              'create_recording': True,
              'presenter_email': teacher['email'],
              'extend_duration': 0,
              #'duration': val,
              'duration': tim,
              'attendee_limit': 2,
              'return_url': domain,
              'status_ping_url': domain
              }
    str_filename = str(question['_id']) + ".json"
    with open(str_filename, 'w') as json_file:
        json.dump(params, json_file)
    os.system('ruby WiZiQServices.rb '+ str_filename)

def AddAttendees(question):
    attendee_list = '<attendee_list>'
    attendee_limit = 2
    class_id = ''
    str_filename = str(question['_id']) + ".json"
    with open(str_filename) as json_file:
        data = json.load(json_file)
        class_id = data['create'][0]['class_details'][0]['class_id'][0]
    for i in range(attendee_limit):
        attendee_list += '<attendee>'
        tem = '<attendee_id><![CDATA[' + str(i + 101) + ']]></attendee_id>' + '<screen_name><![CDATA[Attendee' + str(
            i + 1) + ']]></screen_name>'
        attendee_list += tem
        attendee_list +='<language_culture_name><![CDATA[en-us]]></language_culture_name>'
        attendee_list += '</attendee>'
    attendee_list += '</attendee_list>'
    params = {'method': 'add_attendees',
              'class_id': class_id,
              'attendee_list': attendee_list}
    with open(str_filename, 'w') as json_file:
        json.dump(params, json_file)
    os.system('ruby WiZiQServices.rb '+ str_filename)

# ajax
@app.route('/student/accept', methods=['POST'])
def student_accept():
    res = request.form['data']
    res = json.loads(res)
    teacher_id = res['teacher_id']
    status = res['status']
    question_id = res['question_id']
    question = db_questions.find_one({'_id': ObjectId(question_id)})
    teacher = db_teachers.find_one({'_id':ObjectId(teacher_id)})
    resp = {"success": True}
    if status == 'accept':
        question['status'] = 2
        question['accepted_teacher'] = teacher_id
        m_session = {}
        filename = str(teacher['_id']) + '.json'
        if os.path.isfile(filename):
            os.remove(filename)
        if len(teacher['teacher_id']) == 0:
            add_teacher(teacher_id)
            if os.path.isfile(filename):
                with open(filename) as json_file:
                    data = json.load(json_file)
                    print(data)
                    if 'status' not in data:
                        resp['success'] = False
                        resp['msg'] = "Environment Error : You must install ruby and module before execute." + data
                        print("----------------------Environment Error---------------------------------")
                        print("You must install ruby and module before execute.")
                        if os.path.isfile(filename):
                            os.remove(filename)
                        return jsonify(resp)
                    if data['status'] == 'fail':
                        resp['success'] = False
                        resp['msg'] = data['error'][0]['msg']
                        question['status'] = 1
                        question['accepted_teacher'] = ''
                        for item in question['teachers']:
                            if item['teacher_id'] == teacher_id:
                                item['accept'] = 0
                                break
                        json_file.close()
                        if os.path.isfile(filename):
                            os.remove(filename)
                        db_questions.update({'_id': ObjectId(question_id)}, {"$set": question})
                        return jsonify(resp)
                    if data['status'] == 'ok' and data['method'][0] != 'get_teacher_details':
                        teacher_id1 = data['add_teacher'][0]['teacher_id'][0]
                        teacher['teacher_id'] = teacher_id1
                        db_teachers.update({'_id': ObjectId(teacher_id)}, {"$set": teacher})
                    else:
                        teacher_id1 = data['get_teacher_details'][0]['teacher_details_list'][0]['teacher_details'][0]['teacher_id'][0]
                        teacher['teacher_id'] = teacher_id1
                        db_teachers.update({'_id': ObjectId(teacher_id)}, {"$set": teacher})
            if os.path.isfile(filename):
                os.remove(filename)
        url_temp = request.base_url
        create_class(question, url_temp)
        presenter_url = ''
        recording_url = ''
        class_id = ''
        filename = str(question['_id']) + '.json'
        with open(filename) as json_file:
            data = json.load(json_file)
            if data['status'] == 'fail':
                resp['success'] = False
                resp['msg'] = data['error'][0]['msg']
                question['status'] = 1
                question['accepted_teacher'] = ''
                for item in question['teachers']:
                    if item['teacher_id'] == teacher_id:
                        item['accept'] = 0
                        break
                db_questions.update({'_id': ObjectId(question_id)}, {"$set": question})
                return jsonify(resp)
            presenter_url = data['create'][0]['class_details'][0]['presenter_list'][0]['presenter'][0]['presenter_url'][0]
            recording_url = data['create'][0]['class_details'][0]['recording_url'][0]
            class_id = data['create'][0]['class_details'][0]['class_id'][0]
        m_session['student_id'] = session['user_id']
        m_session['teacher_id'] = teacher_id
        m_session['Start Time'] = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        m_session['Duration'] = 60
        m_session['Price paid'] = 0
        m_session['question id'] = str(question['_id'])
        m_session['video'] = ""
        m_session['Student Rating'] = 0
        m_session['Teacher Rating'] = 0
        teacher_email = db_teachers.find_one({'_id': ObjectId(teacher_id)})
        m_session['presenter_email'] = teacher_email['email']
        m_session['presenter_url'] = presenter_url
        m_session['recording_url'] = recording_url
        domain='http://'+url_temp.split('//')[-1].split('/')[0]+"/review-page"
        m_session['return_url'] = domain
        m_session['status_ping_url'] = domain
        m_session['class_id'] = class_id
        m_session['status'] = 0
        m_session['new_balance'] = 0
        re_session = db_sessions.find_one({"question id":str(question['_id'])})
        if re_session != None:
            db_sessions.update({"question id":str(question['_id'])}, {"$set": m_session})
        else:
            session_id = db_sessions.insert(m_session, check_keys=False)
        print("------------------Create class ---------------------------------")
        print(m_session)
        AddAttendees(question)
        filename = str(question['_id']) + ".json"
        attendee_url = ''
        if os.path.isfile(filename):
            with open(filename) as json_file:
                data = json.load(json_file)
                attendee_url = data['add_attendees'][0]['attendee_list'][0]['attendee'][0]['attendee_url'][0]
        m_session['attendee_url'] = attendee_url
        re_session = db_sessions.find_one({"question id":str(question['_id'])})
        session_id = ""
        if re_session != None:
            db_sessions.update({"question id":str(question['_id'])}, {"$set": m_session})
        else:
            session_id = db_sessions.insert(m_session, check_keys=False)
        if os.path.isfile(filename):
            os.remove(filename)
        p_url = presenter_url
        resp['class_id'] = class_id
        resp['attendee_url'] = attendee_url

    for item in question['teachers']:
        if item['teacher_id'] == teacher_id:
            if status == 'accept':
                item['accept'] = 0
            else:
                item['accept'] = 3
                break
        else:
            if status == 'accept':
                item['accept'] = 3

    db_questions.update({'_id': ObjectId(question_id)}, {"$set": question})
    msg1 = {}
    msg1['header'] = "Welcome to Takweya"
    msg1['body'] = "Hello " + ",there" + ",\nYou can start class now.\n"
    #send_mail(user_info, msg1)
    return jsonify(resp)

@app.route('/student/profile/<string:user_id>', methods=['GET'])
def student_profile(user_id):
    student = db_students.find_one({"_id": ObjectId(user_id)})
    user = {'name': student['First Name'], 'user_id': user_id, 'balance': round(student['Balance'], 2),'user_info':student, 'job': session['job']}
    return render_template('student-profile.html', user=user)

# ajax
@app.route("/student/profile-save",methods=['POST'])
def save_St_profile():
    temp = request.form['data']
    temp = json.loads(temp)
    user_id = str(temp['user_id'])
    student = db_students.find_one({"_id":ObjectId(user_id)})
    if student != None:
        student['First Name'] = temp['First Name']
        student['Last Name'] = temp['Last Name']
        student['Date Of Birth'] = temp['Date Of Birth']
        student['email'] = temp['email']
        student['Phone Number'] = temp['Phone Number']
        student['Telegram'] = temp['Telegram']
        db_students.update({"_id": ObjectId(user_id)}, {"$set": student})
        msg = {"success": True}
        return jsonify(msg)
    else:
        msg = {"success":False}
        return jsonify(msg)

@app.route('/student/find-teacher/<string:question_id>', methods=['GET'])
@slogin_check
def find_teacher(question_id):
    if 'user_id' not in session or session['job'] != 'student':
        return redirect(url_for('login'))
    user_id = session['user_id']
    student = db_students.find_one({"_id": ObjectId(user_id)})
    question = db_questions.find_one({"_id": ObjectId(question_id)})
    if question == None:
        return redirect(url_for('student_dashboard'))
    send_qus = {}
    send_qus['question_id'] = question_id
    send_qus['question'] = question['question']
    send_qus['images'] = question['images']
    send_qus['subject'] = question['subject']
    user = {'name': student['First Name'],'user_id': user_id,'balance':round(student['Balance'],2),'job':'student'}
    return render_template('find-teacher.html', user=user, question=send_qus)
@app.route('/student/question-cancel/<string:question_id>',methods = ["POST"])
def cancel_question_student(question_id):
    question_temp = db_questions.find_one({"_id":ObjectId(question_id)})
    if question_temp != None:
        db_questions.delete_one({"_id":ObjectId(question_id)})
    msg = {"success": True}
    return jsonify(msg)
# ajax
@app.route('/student/receive-proposal', methods=['POST'])
def receive_proposal():
    resp = {'success': True}
    res = request.form['data']
    question = db_questions.find_one({"_id": ObjectId(res)})
    proposals = []
    status = 0  # 0: waiting teacher  1:counting  2:you accepted  3:live   4: closed
    if question['status'] > 1:
        status = question['status']
        if status == 2:
            session1 = db_sessions.find_one({'question id': str(question['_id'])})
            print(session1)
            if session1 != None:
                resp['class_id'] = session1['class_id']
                resp['attendee_url'] = session1['attendee_url']
            else:
                resp['class_id'] = ''
                resp['attendee_url'] = ''
    else:
        for teacher in question['teachers']:
            if teacher['accept'] == 1:
                teacher_db = db_teachers.find_one({"_id": ObjectId(teacher['teacher_id'])})
                proposal = {}
                proposal['teacher_id'] = teacher['teacher_id']
                proposal['photo'] = teacher_db['Photo']
                proposal['teacher_name'] = teacher_db['First Name'] + " " + teacher_db['Last Name']
                proposal['teacher_price'] = teacher_db['hourly']
                proposal['teacher_rating'] = teacher_db['Rating']
                proposal['subject'] = teacher_db['Subjects']
                proposal['Teaching Levels'] = teacher_db['Teaching Levels']
                proposal['experience'] = teacher_db['Experience']
                proposals.append(proposal)
                status = 1
    resp['proposals'] = proposals
    resp['status'] = status
    return jsonify(resp)

@app.route('/session/report/<string:session_id>', methods = ["POST"])
def sendreport(session_id):
    session_temp = db_sessions.find_one({"_id":ObjectId(session_id)})
    session_temp['status'] = 4
    db_sessions.update({"_id": ObjectId(session_id)}, {"$set": session_temp})
    resp = {}
    resp['success'] = True
    resp['msg'] = "Session reported."
    return jsonify(resp)

@app.route('/session-detail/<string:session_id>', methods=['GET'])
def session_detail(session_id):
    if 'user_id' not in session or 'job' not in session:
        return redirect(url_for('login'))
    session_temp = db_sessions.find_one({"_id":ObjectId(session_id)})
    is_online = ""
    show_name = ""
    balance = 0
    if session['job'] == 'admin':
        show_name = 'Admin'
    elif session['job'] == 'student':
        student = db_students.find_one({"_id":ObjectId(session_temp['student_id'])})
        show_name = student['First Name'] + " " + student['Last Name']
        balance = student['Balance']
    else:
        is_online = session['is_online']
        teacher = db_teachers.find_one({"_id":ObjectId(session_temp['teacher_id'])})
        show_name = teacher['First Name'] + " " + teacher['Last Name']
        balance = teacher['balance']
    find_session = {}
    find_session['Start Time'] = datetime.strptime(session_temp['Start Time'], '%d/%m/%Y, %H:%M:%S')
    find_session['Duration'] = round(session_temp['Duration'],2)
    find_session['Price Paid'] = session_temp['Price paid']
    question = db_questions.find_one({"_id":ObjectId(session_temp['question id'])})
    find_session['subject'] = question['subject']
    find_session['question'] = question['question']
    find_session['picture'] = question['images']
    find_session['session_id'] = session_id
    find_session['video'] = session_temp['video']
    find_session['video_download'] = session_temp['recording_url']
    find_session['file_download'] = session_temp['recording_url']
    user = {'name': session['user_name'], 'user_id': session['user_id'], 'is_online': is_online,'job':session['job'], 'show_name':show_name,'balance':round(balance, 2)}
    return render_template('session-detail.html', session_info = find_session, user = user)

@app.route('/send-report', methods=['POST'])
def send_report():
    temp = request.form['data']
    temp = json.loads(temp)
    msg = temp['msg']
    user_email = ""
    if session['job'] == 'student':
        student_temp = db_students.find_one({"_id":ObjectId(session['user_id'])})
        if student_temp != None:
            user_email = student_temp['email']
    elif session['job'] == 'teacher':
        teacher_temp = db_teachers.find_one({"_id":ObjectId(session['user_id'])})
        if teacher_temp != None:
            user_email = teacher_temp['email']
    user_info = {}
    user_info['msg'] = msg
    user_info['name'] = session['user_name']
    user_info['email'] = user_email
    if sendemail_help(user_info):
        resp = {"success": True}
    else:
        resp = {"success": False}
    return jsonify(msg)

@app.route('/help', methods=['GET'])
def help():
    if 'user_id' not in session or 'job' not in session:
        return redirect(url_for('login'))
    balance = 0
    is_online = True
    user_id = session['user_id']
    if session['job'] == 'admin':
        show_name = 'Admin'
    elif session['job'] == 'student':
        student = db_students.find_one({"_id":ObjectId(user_id)})
        show_name = student['First Name'] + " " + student['Last Name']
        balance = student['Balance']
    else:
        is_online = session['is_online']
        teacher = db_teachers.find_one({"_id":ObjectId(user_id)})
        show_name = teacher['First Name'] + " " + teacher['Last Name']
        balance = teacher['balance']

    user = {'name': session['user_name'], 'user_id': session['user_id'], 'is_online': is_online,'job':session['job'], 'show_name':show_name,'balance':round(balance, 2)}
    return render_template('help.html', user = user)

@app.route('/video-download/<string:session_id>' , methods = ["POST"])
def videoDownload(session_id):
    print(session_id)
    session_temp = db_sessions.find_one({'_id':ObjectId(session_id)})
    if session_temp['recording_url'] == "":
        msg = {"success": False, "url":""}
        return jsonify(msg)
    params = {'method':'download',
				'class_id':session_temp['class_id'],
				'recording_format':'zip'
			}
    filename = str(session_id) + ".json"
    with open(filename, 'w') as json_file:
        json.dump(params, json_file)
    os.system('ruby WiZiQServices.rb ' + filename)
    data_url = ""
    with open(filename) as json_file:
        data = json.load(json_file)
        if data['status'] == 'ok':
            item = data["download_recording"][0]["status_xml_path"][0]
            http = urllib3.PoolManager()
            file = http.request('GET', item)
            data = file.data
            data = xmltodict.parse(data)
            data_url = data['rsp']['download_recording']['recording_download_path']
    if os.path.isfile(filename):
        os.remove(filename)
    if data_url == "" or data_url == None:
        msg = {"success":False, "url":""}
        return jsonify(msg)
    msg = {"success": True, "url":data_url}
    return jsonify(msg)
# sign up student
@app.route('/api/student/signup', methods=['GET', 'POST'])
def signupstudent():
    """
    Sign Up page.
    Contains form to sign up as a user on Wisdom platform.
    """
    if request.method == "GET":
        return render_template('Sign-up.html')
    else:
        first_name = request.form['First Name']
        last_name = request.form['Last Name']
        email = request.form['email']
        phonenumber = request.form['Phone Number']
        dob = request.form['Date Of Birth']
        password = request.form['password']
        if first_name is None or email is None or password is None:
            msg = {"status": {"type": "success", "message": "Missing fields"}}
            return jsonify(msg)
        user = db_students.find_one({"email": email})
        if user:
            msg = {"status": {"type": "success", "message": "User already exists"}}
            return jsonify(msg)
        # hash password
        hashed_pw = pwd_context.hash(password)
        data = {"First Name": first_name,
                "Last Name": last_name,
                "email": email,
                "Date Of Birth": dob,
                "Phone Number": phonenumber,
                "password": hashed_pw,
                "Date Signed Up": datetime.utcnow(),
                'Balance': 0,
                'Education Level': 0,
                'Address':'',
                'Rating': 0,
                'Telegram': '',
                'Payment Method': 'Paypal',
                'status':0
                }
        user_id = db_students.insert(data, check_keys=False)
        # create user in logged in table
        data = {"user": str(user_id),
                "is_loggedin": False,
                'is_online': True
                }
        is_loggedin = db_is_loggedin.insert(data, check_keys=False)
        user_info = {'name':first_name, 'email':email,'job':'student'}
        sendemail_signup(user_info)
        # user.hash_password(password)
        msg = {"id": str(user_id)}
        
        return render_template('thankyou.html')

@app.route('/signup', methods=['GET'])
def signup():
    if request.method == "GET":
        return render_template('signupintro.html')

@app.route('/api/phone_check', methods=['POST'])
def phone_check():
    resp = {'success': True}
    temp = request.form['data']
    temp = json.loads(temp)
    phone_number = temp['Phone Number']
    phone_number = phone_number.strip()
    rmatch = re.findall(r"^\+[1-9][0-9]* [0-9]+", phone_number)
    print("------------rmatch--------------")
    print(rmatch)
    if  len(rmatch) == 0 or len(rmatch[0]) != len(phone_number):
        resp['success'] = False
        resp['msg'] = 'Please enter valid phone with country code.<br> For example:+971 555555555'
    return jsonify(resp)

# sign up teacher
@app.route('/api/teacher/signup', methods=['GET', 'POST'])
def signupteacher():
    """
    Sign Up page.
    Contains form to sign up as a user on Wisdom platform.
    """
    if request.method == "GET":
        return render_template('teachersignup.html')
    elif request.method == "POST":
        phone_number = request.form['Phone Number']
        phone_number = phone_number.strip()
        first_name = request.form['First Name']
        last_name = request.form['Last Name']
        date_of_birth = request.form['Date Of Birth']
        graduate = request.form['Graduate']
        experience = request.form['Experience']
        iddocument = request.files['ID']
        certificatedocument = request.files['Certificate']
        additionaldocument = request.files['Document']
        idfilename = secure_filename(iddocument.filename)
        iddocumentid = fs.put(iddocument, content_type=iddocument.content_type, filename=idfilename)
        certificatefilename = secure_filename(certificatedocument.filename)
        certificatedocumentid = fs.put(certificatedocument, content_type=certificatedocument.content_type,
                                       filename=certificatefilename)
        additionalfilename = secure_filename(additionaldocument.filename)
        additionaldocumentid = fs.put(additionaldocument, content_type=additionaldocument.content_type,
                                      filename=additionalfilename)
        gradelevels = request.form.getlist('University')
        subjects = request.form.getlist('Subjects')
        email = request.form['email']
        password = request.form['password']
        if first_name is None or email is None or password is None:
            msg = {"status": {"type": "success", "message": "Missing fields"}}
            return redirect(url_for('signupteacher'))
        user = db_teachers.find_one({"email": email})
        if user:
            msg = {"status": {"type": "success", "message": "User already exists"}}
            return redirect(url_for('signupteacher'))
        # hash password
        hashed_pw = pwd_context.hash(password)
        bank_detail = {
            "receipient name":'',
            "receipient address":'',
            "bank name":'',
            'routing number':'',
            "account number":'',
            'IBAN':''
        }
        data = {"First Name": first_name,
                "Last Name": last_name,
                "balance": 0,
                "Photo": 'avatar.png',
                "email": email,
                "Date Of Birth": date_of_birth,
                "Id Document": iddocumentid,
                "Certificate Document": certificatedocumentid,
                "Additional Document": additionaldocumentid,
                "Teaching Levels": gradelevels,
                "Subjects": subjects,
                "Experience": experience,
                "Graduate": graduate,
                "Phone Number": phone_number,
                "mobile_number":"+1 1234567890",
                'time_zone':'',
                'hourly':10,
                "password": hashed_pw,
                "Date Signed Up": datetime.utcnow(),
                "Rating":0,
                "Address":"",
                "Paypal email":'',
                'Bank detail':bank_detail,
                'teacher_id':'',
                'approve':0,
                }
        user_id = db_teachers.insert(data, check_keys=False)
        user_info = {'name':first_name, 'email':email,'job':'teacher'}
        sendemail_signup(user_info)
        msg = {"id": str(user_id)}
        return redirect(url_for('login'))

# log in 
@app.route('/api/login', methods=['GET', 'POST'])
def login():
    """
    Log In page.
    Contains form to log in to an existing users profile.
    """
    if request.method == "GET":
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        radio = request.form['radio']
        if email == 'admin' and password == 'admin':
            session['user_id'] = 'admin'
            session['user_name'] = 'Admin'
            session['job'] = 'admin'
            return redirect(url_for('admin_page'))
        if radio == 'Student':
            user = db_students.find_one({"email": email})
            if not user:
                flash('Oops! Looks that user does not exist')
                return redirect('login')
            stored_pw = user.get("password")
            if not pwd_context.verify(password, stored_pw):
                flash('Oops! Incorrect username or password')
                return redirect('login')
            first_name = user.get("First Name")
            profile_id = user.get("_id")
            is_loggedin = db_is_loggedin.find_one({"user": str(profile_id)})
            if is_loggedin:
                if is_loggedin.get("is_loggedin") == False:
                    is_loggedin["is_loggedin"] = True
                    db_is_loggedin.update({"user": str(profile_id)}, {"$set": is_loggedin})
                session['job'] = 'student'
                session['user_name'] = first_name
                session['user_id'] = str(profile_id)
                return redirect(url_for('student_dashboard'))
            else:
                flash('Oops! Please wait while approving.')
                return redirect(url_for('login'))

        elif radio == 'Teacher':
            user = db_teachers.find_one({"email": email})
            if not user:
                flash('Oops! Looks that user does not exist')
                return redirect('login')
            stored_pw = user.get("password")
            if not pwd_context.verify(password, stored_pw):
                flash('Oops! Incorrect username or password')
                return redirect('login')
            first_name = user.get("First Name")
            profile_id = user.get("_id")
            is_loggedin = db_is_loggedin.find_one({"user": str(profile_id)})
            if is_loggedin:
                if is_loggedin.get("is_loggedin") == False:
                    is_loggedin["is_loggedin"] = True
                db_is_loggedin.update({"user": str(profile_id)}, {"$set": is_loggedin})
                session['job'] = 'teacher'
                session['user_name'] = first_name
                session['user_id'] = str(profile_id)
                session['is_online'] = is_loggedin["is_online"]
                return redirect(url_for('teacher_dashboard'))
            else:
                flash('Oops! Please wait while approving.')
                return redirect(url_for('login'))

# log out
@app.route('/api/logout', methods=['GET'])
def logout():
    """
    Log Out route.
    Log the user out of their Wisdom account and clear the
    session cookie stored.
    """
    if 'user_id' in session:
        userid = session['user_id']
        is_loggedin = db_is_loggedin.find_one({"user": str(userid)})
        if is_loggedin:
            if is_loggedin.get("is_loggedin") == True:
                data = {"is_loggedin": False}
                db_is_loggedin.update({"user": str(userid)}, {"$set": data})
        session.pop('user_id', None)
    return redirect(url_for('home'))

# login check
@app.route('/api/logincheck/<string:userid>', methods=['GET'])
def logincheck(userid):
    """
    Check whether user is logged in.
    """
    if request.method == "GET":
        if userid:
            is_loggedin = db_is_loggedin.find_one({"user": str(userid)})
            if is_loggedin:
                if is_loggedin.get("is_loggedin") == True:
                    msg = {'id': str(userid)}
                    return jsonify(msg)
                else:
                    msg = {"status": {"type": "success", "message": "User is logged out"}}
                    return jsonify(msg)
            else:
                msg = {"status": {"type": "success", "message": "User not found, sign up"}}
                return jsonify(msg)
        else:
            msg = {"status": {"type": "success", "message": "Provide userid"}}
            return jsonify(msg)

@app.route('/api/user/<string:userid>', methods=['GET'])  # Find student by User ID
def getuser(userid):
    if request.method == "GET":
        user = db_students.find({"_id": ObjectId(userid)})
        user = dumps(user)
        return user

@app.route('/api/login/<string:email>', methods=['GET'])  # Find student by Email Id
def emailuser(email):
    if request.method == "GET":
        user = db_students.find({"email": email})
        user = dumps(user)
        return user

@app.route('/subscribe', methods=['POST'])  # Subscribe
def subscribeemail():
    if request.method == "POST":
        email = request.form['email']
        text = request.form['textarea']
        message = request.form['message']
        phone = request.form['phone']
        print(email)
        print(text)
        return email

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/delete-file', methods=['POST'])
def delete_file():
    resp = {"success": False, 'msg': 'Error while deleting file.'}
    temp = request.form['data']
    fname = os.path.join(dir, app.config['UPLOAD_FOLDER'], temp)
    try:
        if os.path.exists(fname):
            os.remove(fname)
            resp['success'] = True
        else:
            resp['msg'] = 'File does not exit'
    except:
        print("unexpected error while file deleting")
        resp['msg'] = 'Error while deleting'
    return jsonify(resp)

@app.route('/upload-file', methods=['POST'])
def upload_file():
    resp = {'success': True, 'msg': ''}
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp['success'] = False
        resp['msg'] = 'No requested files data'
        return jsonify(resp)

    files = request.files.getlist('files[]')
    errors = {}
    success = False
    res_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ts = str(int(time.time()))
            filename = ts + filename
            temp = os.path.join(dir, app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(temp)
                res_files.append(filename)
                success = True
            except:
                print("Unexpected error while file saving.")
                errors[file.filename] = "Unexpected error while saving"
        else:
            errors[file.filename] = 'File type is not allowed'
    resp = {}
    resp['success'] = success
    resp['files'] = res_files
    resp['errors'] = errors
    resp = jsonify(resp)
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5000)
