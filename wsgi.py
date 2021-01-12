from takweya import app
from flask_socketio import SocketIO
import threading
import time

socketio = SocketIO(app)


count_teachers = []
thread_id = 1
brun = 0
def count_handle(name):
    global count_teachers, brun
    brun = 1
    while(1):
        if len(count_teachers) == 0:
            brun = 0
            break
        for item in count_teachers:
            item['remain_time'] -= 1
            if item['remain_time'] < 1:
                socketio.emit('timeover', item)
                count_teachers.remove(item)
        time.sleep(1)
    
def new_counter():
    global thread_id, brun
    if brun == 0:
        x = threading.Thread(target=count_handle, args=(thread_id,))
        x.start()
        thread_id += 1

@socketio.on('teacher_connect')
def teacher_connect(json):
    global count_teachers
    for item in count_teachers:
        if  item['teacher_id'] == json['user_id']:
            socketio.emit('keep_counting', item)
            break
    
@socketio.on('cancel_proposal')
def cancel_proposal(json):
    global count_teachers
    for item in count_teachers:
        if  item['teacher_id'] == json['user_id']:
            socketio.emit('cancel_proposal', item)
            count_teachers.remove(item)
            break

@socketio.on('cancel_question')
def cancel_question(json):
    socketio.emit('cancel_question', json)
    print("---------------------------canceled questions")
    global count_teachers
    for item in count_teachers:
        if  item['question_id'] == json['question_id']:
            count_teachers.remove(item)

@socketio.on('student_connect')
def student_connect(json):
    print('--- student connected : ' + str(json))

@socketio.on('sendquestion')
def sendquestion(json):
    socketio.emit('sendquestion', json) # let teachers know

@socketio.on('sendquestion_sent')
def sendquestion_sent(json):
    socketio.emit('sendquestion_sent', json) # let teachers know

@socketio.on('teacher_accept')         
def teacher_accept(json):
    global count_teachers
    socketio.emit('teacher_accept', json)   # let student know accepting from teacher
    temp = {'question_id': json['question_id'], 'teacher_id': json['user_id'], 'remain_time' : 5 * 60}
    count_teachers.append(temp)
    new_counter()

@socketio.on('student_accept')
def teacher_accept(json):
    global count_teachers
    socketio.emit('student_accept', json)       # let teacher wait class
    for item in count_teachers:
        if item['question_id'] == json['question_id'] and item['teacher_id'] == json['teacher_id']:
            count_teachers.remove(item)
            break

if __name__ == "__main__":
    #app.run(debug=True)
    socketio.run(app, debug=True)#"host = '192.168.208.183'
