from hashlib import new
from sqlite3 import connect
import pickle
from urllib import response
from wsgiref.simple_server import make_server
from flask import Flask, jsonify, make_response, redirect, render_template, render_template_string, request, request_started
import database
import email_bot
import random

app = Flask(__name__)


@app.route('/bruh')
def bruh():
    return render_template('feed.html', username="sanjiv")


@app.errorhandler(404)
def error_404(e):
    return render_template('error404.html', error = "404")


@app.errorhandler(500)
def error_500(e):
    return render_template('error404.html', error = "500")

@app.route('/admin')
def admin():
    return '''
    <html>
    <head>
    <title>admin page | Slambook</title>
    </head>
    <body>
    <a href="./admin/passwords">passwords database</a>
    <br><br>
    <a href="./admin/users">user database</a>
    </body>
    </html>
    '''

@app.route('/admin/passwords')
def admin_pass():
    return make_response(jsonify(database.get_login_info()), 200)

@app.route('/admin/users')
def admin_users():
    return make_response(jsonify(database.get_all_user_info()), 200)

@app.route('/', methods = ["GET", "POST"])
def function():
    if request.method == "GET":
        if request.cookies.get('login_status') == 'True':
            username = request.cookies.get('login_username')
            rollno = request.cookies.get('login_rollno')
            f = open("./data/posts.bin", "rb")
            all_posts = pickle.load(f)
            f.close()
            f = open("./data/user_data/{rollno}.bin", "rb")
            following, followers = list(pickle.load(f))
            f.close()
            posts = []
            for i in all_posts.values():
                for j in following:
                    if i[0] == username or j in i[1]:
                        posts.append([i[1], i[0]])
            for bruh in range(12):
                bruhh = str(bruh)
                if bruhh not in posts.keys():
                    posts[bruhh] = ["", "", [""], ""]
            return render_template('feed.html', username = username, posts0 = posts[0][0], posts1 = posts[1][0], posts2 = posts[2][0], posts3 = posts[3][0], posts4 = posts[4][0], posts5 = posts[5][0], posts6 = posts[6][0], posts7 = posts[7][0], posts8 = posts[8][0], posts9 = posts[9][0], posts10 = posts[10][0], postby0 = posts[0][1], postby1 = posts[1][0], postby2 = posts[2][1], postby3 = posts[3][1], postby4 = posts[4][1], postby5 = posts[5][1], postby6 = posts[6][1], postby7 = posts[7][1], postby8 = posts[8][1], postby9 = posts[9][1], postby10 = posts[10][1])
        else:
            return render_template('login.html')
    if request.method == "POST":
        search_content = str(request.form.get("search_bar"))
        new_post_content = str(request.form.get("new_post_bar"))
        print(search_content)
        print(new_post_content)
        if search_content != "":
            return redirect("/search")
        if new_post_content != "":
            pass
        return redirect("/")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/developer')
def developer_information():
    return render_template('developer.html')

@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login_validation():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        content = database.get_login_info()
        rollno = str(request.form.get('rollno'))
        password = str(request.form.get('password'))
        #print('\n\n\n\n{}\n\n{}\n\n\n\n'.format(len(rollno), len(password)))
        #return "username = {} password = {}".format(rollno, password)
        if content[rollno] == password:
            res = make_response(render_template('login_success.html'))
            username = database.get_user_info(rollno)['username']
            res.set_cookie('loginstatus', 'True')
            res.set_cookie('login_rollno', rollno)
            res.set_cookie('login_username', username)
            return res
        else:
            return make_response(render_template("login.html"))


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    if request.method == "POST":
        name = str(request.form.get('name'))
        rollno = str(request.form.get('rollno'))
        password1 = str(request.form.get('password1'))
        password2 = str(request.form.get('password2'))
        gender = str(request.form.get('gender'))
        programme = str(request.form.get('programme'))
        branch = str(request.form.get('branch'))
        section = str(request.form.get('section'))
        username = str(request.form.get('username'))
        hostel = str(request.form.get('hostel'))
        f = open("./data/user_data/{rollno}.bin", "wb")
        content = [["slambook"], []]  #[[following], [followers]]
        pickle.dump(content, f)
        f.close()
        if database.check_signup(name, rollno, password1, password2, gender, programme, branch, section, username, hostel)[0]:
            return render_template('signup_success.html')
        else:
            return database.check_signup(name, rollno, password1, password2, gender, programme, branch, section, username, hostel)[1]


@app.route('/logout', methods=["POST", "GET"])
def logout():
    if request.method == 'GET':
        res = make_response(redirect('./login'))
        res.set_cookie('loginstatus', "false")
        res.set_cookie('login_rollno', '')
        res.set_cookie('login_username', '')
        return res

@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")
    if request.method == "POST":
        rollno = request.form.get('rollno')
        f = open('./data/otp.bin', "wb")
        otp = str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))+str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))+str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))+str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
        print(otp)
        pickle.dump([rollno, otp], f)
        f.close()
        email_bot.send_otp(str(rollno)+"@nitt.edu", otp)
        return render_template("forgot_password_step_2.html")

@app.route('/forgot_password/otp_accepted', methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template('forgot_password_Step_2.html')
    if request.method == "POST":
        f = open("./data/otp.bin", 'rb')
        rollno, given_otp = list(pickle.load(f))
        f.close()
        otp = request.form.get('otp')
        newpassword1 = request.form.get('newpassword1')
        newpassword2 = request.form.get('newpassword2')
        if otp == given_otp and newpassword1 == newpassword2:
            database.put_login_info(rollno, newpassword1)
            return render_template('password_changed.html')
        else:
            return "error"



@app.route('/my_profile', methods=["POST", "GET"])
def my_profile():
    return render_template('my_profile.html')


@app.route('/settings', methods=["POST", "GET"])
def settings():
    return render_template('settings.html')


'''
@app.route('/login_bypass', methods = ['POST', 'GET'])
def login_bypass():
    if True: #request.method == 'POST':
        user = 'True'   # request.form['login_status']
        resp = make_response(render_template('login_success.html'))
        resp.set_cookie('login_status', user)
        return resp
    return "cookie not found"
'''



   
if __name__ == '__main__':
    app.run(port='5000')