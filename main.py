from crypt import methods
from encodings import search_function
from hashlib import new
from operator import methodcaller
import re
from sqlite3 import connect
import pickle
from urllib import response
from wsgiref.simple_server import make_server
from flask import Flask, jsonify, make_response, redirect, render_template, request
import database
import email_bot
import random

app = Flask(__name__)


@app.route('/bruh')
def bruh():
    return render_template('feed.html', username="sanjiv")

@app.errorhandler(403)
def error_403(e):
    return render_template('error404.html', error = "403")

@app.errorhandler(404)
def error_404(e):
    return render_template('error404.html', error = "404")


@app.errorhandler(500)
def error_500(e):
    return render_template('error404.html', error = "500")

@app.route('/admin')
def admin_access_denied():
    return render_template('error404.html', error = "403")

@app.route('/admin/sanjiv')
def admin():
    return '''
    <html>
    <head>
    <title>admin page | Slambook</title>
    </head>
    <body>
    <a href="/admin/sanjiv/passwords">passwords database</a>
    <br><br>
    <a href="/admin/sanjiv/users">user database</a>
    <br><br>
    <a href="/admin/sanjiv/posts">all posts</a>
    <br><br>
    <a href="/admin/sanjiv/follow">all profile following and followers list</a>
    </body>
    </html>
    '''

@app.route('/admin/sanjiv/passwords')
def admin_pass():
    return make_response(jsonify(database.get_login_info()), 200)

@app.route('/admin/sanjiv/users')
def admin_users():
    return make_response(jsonify(database.get_all_user_info()), 200)

@app.route('/admin/sanjiv/posts')
def admin_posts():
    return make_response(jsonify(database.get_all_posts()), 200)

@app.route('/admin/sanjiv/follow')
def admin_follow():
    return make_response(jsonify(database.get_follow()), 200)



@app.route('/', methods = ["GET", "POST"])
def function():
    if request.method == "GET":
        if request.cookies.get('login_status') == 'True':
            username = request.cookies.get('login_username')
            rollno = request.cookies.get('login_rollno')
            f = open("./data/posts.bin", "rb")
            all_posts = list(pickle.load(f))[::-1]    #[["by", "message", ["tags"...], "timestamp"]...]
            f.close()
            f = open("./data/user_data/{}.bin".format(rollno), "rb")
            following = list(pickle.load(f))
            f.close()
            posts = []
            if len(following) == 0:
                posts = [[["search and follow your friends to see their posts"], ["slambook"]]]
            else:
                for i in all_posts:
                    for j in following:
                        if i[1] not in [bruh[0] for bruh in posts] and (i[0] == username or j in i[1] or rollno in i[1]):
                            #posts.append([i[1], i[0]])
                            posts.append([database.change_rollno_to_username(i[1]), database.change_rollno_to_username(i[0]), len(all_posts)-1-all_posts.index(i)])
            for bruh in range(31-len(posts)):
                posts.append(["", "", ""])
            return render_template('feed.html', rollno = rollno, username = username, post0 = posts[0][0], postby0 = posts[0][1], postID0 = posts[0][2], post1 = posts[1][0], postby1 = posts[1][1], postID1 = posts[1][2], post2 = posts[2][0], postby2 = posts[2][1], postID2 = posts[2][2], post3 = posts[3][0], postby3 = posts[3][1], postID3 = posts[3][2], post4 = posts[4][0], postby4 = posts[4][1], postID4 = posts[4][2], post5 = posts[5][0], postby5 = posts[5][1], postID5 = posts[5][2], post6 = posts[6][0], postby6 = posts[6][1], postID6 = posts[6][2], post7 = posts[7][0], postby7 = posts[7][1], postID7 = posts[7][2], post8 = posts[8][0], postby8 = posts[8][1], postID8 = posts[8][2], post9 = posts[9][0], postby9 = posts[9][1], postID9 = posts[9][2], post10 = posts[10][0], postby10 = posts[10][1], postID10 = posts[10][2], post11 = posts[11][0], postby11 = posts[11][1], postID11 = posts[11][2], post12 = posts[12][0], postby12 = posts[12][1], postID12 = posts[12][2], post13 = posts[13][0], postby13 = posts[13][1], postID13 = posts[13][2], post14 = posts[14][0], postby14 = posts[14][1], postID14 = posts[14][2], post15 = posts[15][0], postby15 = posts[15][1], postID15 = posts[15][2], post16 = posts[16][0], postby16 = posts[16][1], postID16 = posts[16][2], post17 = posts[17][0], postby17 = posts[17][1], postID17 = posts[17][2], post18 = posts[18][0], postby18 = posts[18][1], postID18 = posts[18][2], post19 = posts[19][0], postby19 = posts[19][1], postID19 = posts[19][2], post20 = posts[20][0], postby20 = posts[20][1], postID20 = posts[20][2], post21 = posts[21][0], postby21 = posts[21][1], postID21 = posts[21][2], post22 = posts[22][0], postby22 = posts[22][1], postID22 = posts[22][2], post23 = posts[23][0], postby23 = posts[23][1], postID23 = posts[23][2], post24 = posts[24][0], postby24 = posts[24][1], postID24 = posts[24][2], post25 = posts[25][0], postby25 = posts[25][1], postID25 = posts[25][2], post26 = posts[26][0], postby26 = posts[26][1], postID26 = posts[26][2], post27 = posts[27][0], postby27 = posts[27][1], postID27 = posts[27][2], post28 = posts[28][0], postby28 = posts[28][1], postID28 = posts[28][2], post29 = posts[29][0], postby29 = posts[29][1], postID29 = posts[29][2], post30 = posts[30][0], postby30 = posts[30][1], postID30 = posts[30][2])
            # return render_template('feed.html', username = username, posts0 = "sanjiv", postby0 = "sanjiv", posts1 = "", postby1 = "")
        else:
            return redirect('./login')
    if request.method == "POST":
        search_content = str(request.form.get("search_bar"))
        new_post_content = str(request.form.get("new_post_bar"))
        print(search_content)
        print(new_post_content)
        if search_content != "None":
            f = open("./data/search.bin", "wb")
            pickle.dump(search_content, f)
            f.close()
            res = make_response(redirect('/search_result'))
            res.set_cookie("branch", "None")
            res.set_cookie("section", "None")
            res.set_cookie("hostel", "None")
            return res
        if new_post_content != "None":
            print("making a new post")
            database.push_new_post(new_post_content, str(request.cookies.get('login_username')))
            return redirect("/")
        return redirect("/")

@app.route("/search_result", methods = ["GET", "POST"])
def search_result():
    if request.method == "GET":
        f = open("./data/search.bin", "rb")
        search_content = str(pickle.load(f)).split()
        f.close()
        f = open("./data/user_info.bin", "rb")
        user_info = dict(pickle.load(f))
        f.close()
        rollno = request.cookies.get('login_rollno')
        branch = request.cookies.get("branch")
        section = request.cookies.get("section")
        hostel = request.cookies.get("hostel")
        search_result = []
        for i in user_info.values():
            name = i['name'].split(" ")
            username = i['username'].split(" ")
            for search_content_element in search_content:
                for name_element in name:
                    if search_content_element == name_element:
                        search_result.append(i)
            for search_content_element in search_content:
                for name_element in username:
                    if search_content_element == name_element:
                        search_result.append(i)
        final = []
        if branch != 'None' and section != "None" and hostel != 'None':
            for i in search_result:
                if i['branch'] == branch and i['section'] == section and i["hostel"] == hostel and i not in final:
                    final.append(i)
        if branch != 'None' and section != "None" and hostel == 'None':
            for i in search_result:
                if i['branch'] == branch and i['section'] == section and i not in final:
                    final.append(i)
        if branch != 'None' and section == "None" and hostel != 'None':
            for i in search_result:
                if i['branch'] == branch and i["hostel"] == hostel and i not in final:
                    final.append(i)
        if branch == 'None' and section != "None" and hostel != 'None':
            for i in search_result:
                if i['section'] == section and i["hostel"] == hostel and i not in final:
                    final.append(i)
        if branch != 'None' and section == "None" and hostel == 'None':
            for i in search_result:
                if i['branch'] == branch and i not in final:
                    final.append(i)
        if branch == 'None' and section != "None" and hostel == 'None':
            for i in search_result:
                if i['section'] == section and i not in final:
                    final.append(i)
        if branch == 'None' and section == "None" and hostel != 'None':
            for i in search_result:
                if i["hostel"] == hostel and i not in final:
                    final.append(i)   
        if branch == 'None' and section == 'None' and hostel == 'None':
            final = list(search_result)
        print(final)
        for i in range(31 - len(final)):
            final.append({"name" : "", "gender" : "", "programme" : "", "branch" : "", "section" : "", "username" : "", "hostel" : "", "rollno": ""})
        return render_template('search_result.html', rollno = rollno, username = str(request.cookies.get('login_username')), rollno0 = final[0]['rollno'], user0 = final[0]['username'], dept0 = final[0]['branch'] + ' ' + final[0]['section'], rollno1 = final[1]['rollno'], user1 = final[1]['username'], dept1 = final[1]['branch'] + ' ' + final[1]['section'], rollno2 = final[2]['rollno'], user2 = final[2]['username'], dept2 = final[2]['branch'] + ' ' + final[2]['section'], rollno3 = final[3]['rollno'], user3 = final[3]['username'], dept3 = final[3]['branch'] + ' ' + final[3]['section'], rollno4 = final[4]['rollno'], user4 = final[4]['username'], dept4 = final[4]['branch'] + ' ' + final[4]['section'], rollno5 = final[5]['rollno'], user5 = final[5]['username'], dept5 = final[5]['branch'] + ' ' + final[5]['section'], rollno6 = final[6]['rollno'], user6 = final[6]['username'], dept6 = final[6]['branch'] + ' ' + final[6]['section'], rollno7 = final[7]['rollno'], user7 = final[7]['username'], dept7 = final[7]['branch'] + ' ' + final[7]['section'], rollno8 = final[8]['rollno'], user8 = final[8]['username'], dept8 = final[8]['branch'] + ' ' + final[8]['section'], rollno9 = final[9]['rollno'], user9 = final[9]['username'], dept9 = final[9]['branch'] + ' ' + final[9]['section'], rollno10 = final[10]['rollno'], user10 = final[10]['username'], dept10 = final[10]['branch'] + ' ' + final[10]['section'], rollno11 = final[11]['rollno'], user11 = final[11]['username'], dept11 = final[11]['branch'] + ' ' + final[11]['section'], rollno12 = final[12]['rollno'], user12 = final[12]['username'], dept12 = final[12]['branch'] + ' ' + final[12]['section'], rollno13 = final[13]['rollno'], user13 = final[13]['username'], dept13 = final[13]['branch'] + ' ' + final[13]['section'], rollno14 = final[14]['rollno'], user14 = final[14]['username'], dept14 = final[14]['branch'] + ' ' + final[14]['section'], rollno15 = final[15]['rollno'], user15 = final[15]['username'], dept15 = final[15]['branch'] + ' ' + final[15]['section'], rollno16 = final[16]['rollno'], user16 = final[16]['username'], dept16 = final[16]['branch'] + ' ' + final[16]['section'], rollno17 = final[17]['rollno'], user17 = final[17]['username'], dept17 = final[17]['branch'] + ' ' + final[17]['section'], rollno18 = final[18]['rollno'], user18 = final[18]['username'], dept18 = final[18]['branch'] + ' ' + final[18]['section'], rollno19 = final[19]['rollno'], user19 = final[19]['username'], dept19 = final[19]['branch'] + ' ' + final[19]['section'], rollno20 = final[20]['rollno'], user20 = final[20]['username'], dept20 = final[20]['branch'] + ' ' + final[20]['section'], rollno21 = final[21]['rollno'], user21 = final[21]['username'], dept21 = final[21]['branch'] + ' ' + final[21]['section'], rollno22 = final[22]['rollno'], user22 = final[22]['username'], dept22 = final[22]['branch'] + ' ' + final[22]['section'], rollno23 = final[23]['rollno'], user23 = final[23]['username'], dept23 = final[23]['branch'] + ' ' + final[23]['section'], rollno24 = final[24]['rollno'], user24 = final[24]['username'], dept24 = final[24]['branch'] + ' ' + final[24]['section'], rollno25 = final[25]['rollno'], user25 = final[25]['username'], dept25 = final[25]['branch'] + ' ' + final[25]['section'], rollno26 = final[26]['rollno'], user26 = final[26]['username'], dept26 = final[26]['branch'] + ' ' + final[26]['section'], rollno27 = final[27]['rollno'], user27 = final[27]['username'], dept27 = final[27]['branch'] + ' ' + final[27]['section'], rollno28 = final[28]['rollno'], user28 = final[28]['username'], dept28 = final[28]['branch'] + ' ' + final[28]['section'], rollno29 = final[29]['rollno'], user29 = final[29]['username'], dept29 = final[29]['branch'] + ' ' + final[29]['section'], rollno30 = final[30]['rollno'], user30 = final[30]['username'], dept30 = final[30]['branch'] + ' ' + final[30]['section'])
    if request.method == "POST":
        search_content = str(request.form.get("search_bar"))
        f = open("./data/search.bin", "wb")
        pickle.dump(search_content, f)
        f.close()
        res = make_response(redirect('/search_result'))
        res.set_cookie("branch", request.form.get('branch'))
        res.set_cookie("section", request.form.get('section'))
        res.set_cookie("hostel", request.form.get('hostel'))
        return res




@app.route('/profile/<rollno>', methods=["GET", "POST"])
def user_profile(rollno):
    if request.method == "GET":
        f = open("./data/user_info.bin", "rb")
        content = pickle.load(f)
        f.close()
        f = open("./data/posts.bin", "rb")
        all_posts = list(pickle.load(f))[::-1]    #[["by", "message", ["tags"...], "timestamp"]...]
        f.close()
        f = open("./data/user_data/{}.bin".format(request.cookies.get('login_rollno')), "rb")
        following = list(pickle.load(f))
        f.close()
        if rollno in following:
            follow_or_unfollow = 'Unfollow'
        else:
            follow_or_unfollow = "Follow"
        posts = []
        for i in all_posts:
            if i[0] == "@"+rollno or "@"+rollno in i[2]:
                #posts.append([i[1], i[0]])
                posts.append([database.change_rollno_to_username(i[1]), database.change_rollno_to_username(i[0]), len(all_posts)-1-all_posts.index(i)])
        if len(posts) == 0:
            posts = [["NO POSTS", "", ""]]
        for bruh in range(31-len(posts)):
            posts.append(["", "", ""])
        username = content[rollno]['username']
        name = content[rollno]['name']
        dept = content[rollno]['branch'] + " " + content[rollno]['section']
        return render_template("profile.html", login_username = request.cookies.get('login_username'), rollno = rollno, name = name, username = username, dept =  dept, follow_or_unfollow = follow_or_unfollow + " " + username, post0 = posts[0][0], postby0 = posts[0][1], postID0 = posts[0][2], post1 = posts[1][0], postby1 = posts[1][1], postID1 = posts[1][2], post2 = posts[2][0], postby2 = posts[2][1], postID2 = posts[2][2], post3 = posts[3][0], postby3 = posts[3][1], postID3 = posts[3][2], post4 = posts[4][0], postby4 = posts[4][1], postID4 = posts[4][2], post5 = posts[5][0], postby5 = posts[5][1], postID5 = posts[5][2], post6 = posts[6][0], postby6 = posts[6][1], postID6 = posts[6][2], post7 = posts[7][0], postby7 = posts[7][1], postID7 = posts[7][2], post8 = posts[8][0], postby8 = posts[8][1], postID8 = posts[8][2], post9 = posts[9][0], postby9 = posts[9][1], postID9 = posts[9][2], post10 = posts[10][0], postby10 = posts[10][1], postID10 = posts[10][2], post11 = posts[11][0], postby11 = posts[11][1], postID11 = posts[11][2], post12 = posts[12][0], postby12 = posts[12][1], postID12 = posts[12][2], post13 = posts[13][0], postby13 = posts[13][1], postID13 = posts[13][2], post14 = posts[14][0], postby14 = posts[14][1], postID14 = posts[14][2], post15 = posts[15][0], postby15 = posts[15][1], postID15 = posts[15][2], post16 = posts[16][0], postby16 = posts[16][1], postID16 = posts[16][2], post17 = posts[17][0], postby17 = posts[17][1], postID17 = posts[17][2], post18 = posts[18][0], postby18 = posts[18][1], postID18 = posts[18][2], post19 = posts[19][0], postby19 = posts[19][1], postID19 = posts[19][2], post20 = posts[20][0], postby20 = posts[20][1], postID20 = posts[20][2], post21 = posts[21][0], postby21 = posts[21][1], postID21 = posts[21][2], post22 = posts[22][0], postby22 = posts[22][1], postID22 = posts[22][2], post23 = posts[23][0], postby23 = posts[23][1], postID23 = posts[23][2], post24 = posts[24][0], postby24 = posts[24][1], postID24 = posts[24][2], post25 = posts[25][0], postby25 = posts[25][1], postID25 = posts[25][2], post26 = posts[26][0], postby26 = posts[26][1], postID26 = posts[26][2], post27 = posts[27][0], postby27 = posts[27][1], postID27 = posts[27][2], post28 = posts[28][0], postby28 = posts[28][1], postID28 = posts[28][2], post29 = posts[29][0], postby29 = posts[29][1], postID29 = posts[29][2], post30 = posts[30][0], postby30 = posts[30][1], postID30 = posts[30][2])
    if request.method == "POST":
        f = open("./data/user_data/{}.bin".format(request.cookies.get('login_rollno')), "rb")
        content = list(pickle.load(f))
        f.close()
        if rollno in content:
            content.remove(rollno)
        else:
            content.append(rollno)
        f = open("./data/user_data/{}.bin".format(request.cookies.get('login_rollno')), "wb")
        pickle.dump(content, f)
        f.close()
        return redirect('/profile/{}'.format(rollno))


@app.route('/follow_list/<rollno>', methods=["GET"])
def follow_list(rollno):
    f = open("./data/user_info.bin", "rb")
    content = pickle.load(f)
    f.close()
    username = content[rollno]['username']
    name = content[rollno]['name']
    dept = content[rollno]['branch'] + " " + content[rollno]['section']
    followings, followers = database.followings_followers_list(rollno)
    for i in range(101 - len(followings)):
        followings.append("")
        followers.append("")
    return render_template('followers_list.html', login_rollno = request.cookies.get("login_rollno"), username = username, name = name, dept = dept, login_username = request.cookies.get('login_username'), rollno = rollno, follower0 = followers[0], following0 = followings[0], follower1 = followers[1], following1 = followings[1], follower2 = followers[2], following2 = followings[2], follower3 = followers[3], following3 = followings[3], follower4 = followers[4], following4 = followings[4], follower5 = followers[5], following5 = followings[5], follower6 = followers[6], following6 = followings[6], follower7 = followers[7], following7 = followings[7], follower8 = followers[8], following8 = followings[8], follower9 = followers[9], following9 = followings[9], follower10 = followers[10], following10 = followings[10], follower11 = followers[11], following11 = followings[11], follower12 = followers[12], following12 = followings[12], follower13 = followers[13], following13 = followings[13], follower14 = followers[14], following14 = followings[14], follower15 = followers[15], following15 = followings[15], follower16 = followers[16], following16 = followings[16], follower17 = followers[17], following17 = followings[17], follower18 = followers[18], following18 = followings[18], follower19 = followers[19], following19 = followings[19], follower20 = followers[20], following20 = followings[20], follower21 = followers[21], following21 = followings[21], follower22 = followers[22], following22 = followings[22], follower23 = followers[23], following23 = followings[23], follower24 = followers[24], following24 = followings[24], follower25 = followers[25], following25 = followings[25], follower26 = followers[26], following26 = followings[26], follower27 = followers[27], following27 = followings[27], follower28 = followers[28], following28 = followings[28], follower29 = followers[29], following29 = followings[29], follower30 = followers[30], following30 = followings[30], follower31 = followers[31], following31 = followings[31], follower32 = followers[32], following32 = followings[32], follower33 = followers[33], following33 = followings[33], follower34 = followers[34], following34 = followings[34], follower35 = followers[35], following35 = followings[35], follower36 = followers[36], following36 = followings[36], follower37 = followers[37], following37 = followings[37], follower38 = followers[38], following38 = followings[38], follower39 = followers[39], following39 = followings[39], follower40 = followers[40], following40 = followings[40], follower41 = followers[41], following41 = followings[41], follower42 = followers[42], following42 = followings[42], follower43 = followers[43], following43 = followings[43], follower44 = followers[44], following44 = followings[44], follower45 = followers[45], following45 = followings[45], follower46 = followers[46], following46 = followings[46], follower47 = followers[47], following47 = followings[47], follower48 = followers[48], following48 = followings[48], follower49 = followers[49], following49 = followings[49], follower50 = followers[50], following50 = followings[50], follower51 = followers[51], following51 = followings[51], follower52 = followers[52], following52 = followings[52], follower53 = followers[53], following53 = followings[53], follower54 = followers[54], following54 = followings[54], follower55 = followers[55], following55 = followings[55], follower56 = followers[56], following56 = followings[56], follower57 = followers[57], following57 = followings[57], follower58 = followers[58], following58 = followings[58], follower59 = followers[59], following59 = followings[59], follower60 = followers[60], following60 = followings[60], follower61 = followers[61], following61 = followings[61], follower62 = followers[62], following62 = followings[62], follower63 = followers[63], following63 = followings[63], follower64 = followers[64], following64 = followings[64], follower65 = followers[65], following65 = followings[65], follower66 = followers[66], following66 = followings[66], follower67 = followers[67], following67 = followings[67], follower68 = followers[68], following68 = followings[68], follower69 = followers[69], following69 = followings[69], follower70 = followers[70], following70 = followings[70], follower71 = followers[71], following71 = followings[71], follower72 = followers[72], following72 = followings[72], follower73 = followers[73], following73 = followings[73], follower74 = followers[74], following74 = followings[74], follower75 = followers[75], following75 = followings[75], follower76 = followers[76], following76 = followings[76], follower77 = followers[77], following77 = followings[77], follower78 = followers[78], following78 = followings[78], follower79 = followers[79], following79 = followings[79], follower80 = followers[80], following80 = followings[80], follower81 = followers[81], following81 = followings[81], follower82 = followers[82], following82 = followings[82], follower83 = followers[83], following83 = followings[83], follower84 = followers[84], following84 = followings[84], follower85 = followers[85], following85 = followings[85], follower86 = followers[86], following86 = followings[86], follower87 = followers[87], following87 = followings[87], follower88 = followers[88], following88 = followings[88], follower89 = followers[89], following89 = followings[89], follower90 = followers[90], following90 = followings[90], follower91 = followers[91], following91 = followings[91], follower92 = followers[92], following92 = followings[92], follower93 = followers[93], following93 = followings[93], follower94 = followers[94], following94 = followings[94], follower95 = followers[95], following95 = followings[95], follower96 = followers[96], following96 = followings[96], follower97 = followers[97], following97 = followings[97], follower98 = followers[98], following98 = followings[98], follower99 = followers[99], following99 = followings[99], follower100 = followers[100], following100 = followings[100])



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
        if rollno not in content.keys():
            return make_response(redirect("/login"))
        if content[rollno] == password:
            res = make_response(render_template('login_success.html'))
            username = database.get_user_info(rollno)['username']
            res.set_cookie('login_status', 'True')
            res.set_cookie('login_rollno', rollno)
            res.set_cookie('login_username', username)
            return res
        else:
            return redirect("./login")


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
        name.replace(" ", "_")
        f = open("./data/user_data/{}.bin".format(rollno), "wb")
        content = []  #[following]
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
        res.set_cookie('login_status', "false")
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
    return redirect("/profile/{}".format(request.cookies.get('login_username')))


@app.route('/settings', methods=["POST", "GET"])
def settings():
    if request.method == "GET":
        return render_template('settings.html', username = request.cookies.get('login_username'))
    if request.method == "POST":
        post_number = str(request.form.get('post_number'))
        old_password = str(request.form.get('old_password'))
        new_password1 = str(request.form.get('new_password1'))
        new_password2 = str(request.form.get('new_password2'))
        if post_number != "None":
            database.del_post(post_number)
            return redirect('/settings')
        if old_password != "None" or new_password1 != "None" or new_password2 != "None":
            rollno = request.cookies.get('login_rollno')
            database.change_password(rollno = rollno, old_password = old_password, new_password1 = new_password1, new_password2 = new_password2)
            return redirect('/setings')









   
if __name__ == '__main__':
    app.run(port='5000')