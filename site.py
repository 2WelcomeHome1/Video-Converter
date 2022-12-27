from flask import *
import  os, subprocess, time, threading, random
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'user' in session or not session ['user'] in users:
            return "Fucking no name, please, register an account"
        return f(*args, **kwargs)
    return decorated_function

app = Flask("video")
app.secret_key = "123456sdfghjkldfkvns"

class Video:
    def __init__(self):
        self.input = ""
        self.output = ""
        self.user = ""
        self.status = 0
        self.start_time = 0
        self.duration_time = 0
class User:
    def __init__(self, username, password):
        self.username =  username
        self.password = password
        self.videos = []

users = {'admin': User('admin','12333')}

queue = []
def worker():
    global queue, users
    while 1:
        if len(queue) == 0:
            time.sleep (5)
            continue

        vid = queue [0]
        queue = queue [1:]

        user = vid.user
        start_time = vid.start_time
        duration_time = vid.duration_time

        filename = vid.input
        in_filename = os.path.join ('origin', filename)
        rnd = str(random.randint (1000, 9999))
        outname = filename + '.' + rnd +'.gif'
        out_filename = os.path.join ('converted', outname)

        
        cmd = f'ffmpeg -ss {start_time} -t {duration_time} -i {in_filename} -vf "fps=10,scale=320:-1:'+\
            f'flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 {out_filename}' 
        
        vid.status = "in process"
        proc = subprocess.Popen (cmd, shell=True)
        proc.communicate ()
        vid.output = outname
        vid.status = "ready"

NUM_TH = 1
ths=[]
for i in range (NUM_TH):
    t = threading.Thread(target=worker)
    ths.append(t)
    t.daemon = True
    t.start()

@app.route("/")
def main_page():
    global queue, users
    username = ''
    if 'username' in session and session ['username'] in users:
        username = session ['username']
        return render_template ('index.html', username = username)
    return render_template ('index.html')

         


@app.route("/register", methods = ['POST'])
def register() :
    global queue, users
    username = request.values ['username']
    password = request.values ['password']
    print(username, password)
    if username in users:
        return jsonify (dict(status = "Something went wrong !", message = "User '%s' already exist." %username))
    users[username] = User (username, password)
    return jsonify (dict(status = "Congratulations !", message = "User %s successfuly registered" %username))

@app.route("/login", methods = ['POST'])
def login ():
    global queue, users
    username = request.values ['username']
    password = request.values ['password']
    if username in users:
        if users [username].password == password :
            session ['username'] = username
            return  jsonify (dict(status = "Congratulations!", message = "User %s successfuly logged In" %username))
        else:
            return  jsonify (dict(status = "Your misclick, bro! " , message = "Invalid password" ))
    else:
        return jsonify (dict(status = "No such user, man!" , message = "Why do you want to fool me ?"))

@app.route("/logout")
def log_out ():
    print ("Log out")
    del session ['username']
    print ("Del session")
    print ("Open main page")
    return redirect ("/")

@app.route ("/convert", methods = ["POST"])
def convert ():
    global queue, users
    start_time = request.values ['start_time']
    duration_time = request.values ['duration']
    user_file = request.files ['user_video']
    fname = user_file.filename
    store_path = os.path.join ("origin", fname)
    user_file.save(store_path)
    print (request.values)
    print (request.files)
    vid = Video ()
    users [session ['username']].videos.append (vid)
    vid.user =  users [session ['username']]
    vid.input = fname
    vid.status =  "pending"
    vid.start_time = start_time
    vid.duration_time = duration_time
    queue.append (vid)
    return jsonify (dict(status = "OK" , message = "Uploaded"))


@app.route ("/status")
def status ():
    global queue, users
    data = []
    user = users [session ['username']]
    for vid in user.videos :
        el={}
        el ['input'] = vid.input
        el ['status'] = vid.status
        el ['output'] = vid.output
        data.append (el)
    return jsonify (dict(status = "OK" , data = data))

@app.route ("/out/<fname>")
@login_required
def download_link (fname):
    return send_from_directory("converted", fname)

app.run(host ="0.0.0.0", port = 8321, debug=True)