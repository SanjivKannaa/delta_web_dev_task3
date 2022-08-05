from gettext import find
from webbrowser import get
from cryptography.fernet import Fernet
import pickle
import csv
import os
from flask import message_flashed
import datetime


def init():
    f = open("./data/login_info.bin", "wb")
    content = {
        "106121116":encry("madhumitha"),
        "110121111":encry("password")
    }
    pickle.dump(content, f)
    f.close()
    f = open("./data/user_info.bin", "wb")
    content = {
        "106121116" : {
            "name" : "sanjiv kannaa jeganathan",
            "gender" : "MALE",
            "programme" : "B.TECH",
            "branch" : "CSE",
            "section" : "B",
            "username" : "sanjiv_kannaa_jeganathan",
            "hostel" : "zircon b"
        },
        "110121111" : {
            "name" : "madhumitha t e",
            "gender" : "FEMALE",
            "programme" : "B.TECH",
            "branch" : "ICE",
            "section" : "A",
            "username" : "madhuxmitha",
            "hostel" : "opal D"
        }
    }
    pickle.dump(content, f)
    f.close()

def encry(data):
    file = "./data/encryption_key.bin"
    f = open(file, "rb")
    key = pickle.load(f)
    f.close()
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

def decry(data):
    file = "./data/encryption_key.bin"
    f = open(file, "rb")
    key = pickle.load(f)
    f.close()
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()


def put_login_info(rollno, password):
    try:
        f = open("./data/login_info.bin", "rb")
        content = dict(pickle.load(f))
        f.close()
        content[str(rollno)] = encry(password)
        f = open("./data/login_info.bin", "wb")
        pickle.dump(content, f)
        f.close()
    except:
        f = open("./data/login_info.bin", "wb")
        content = {str(rollno) : encry(password)}
        pickle.dump(content, f)
        f.close()


def get_login_info():
    f = open("./data/login_info.bin", "rb")
    content = dict(pickle.load(f))
    f.close()
    content2 = {}
    for i in content:
        content2[i] = decry(content[i])
    return content2


def get_all_user_info():
    f = open("./data/user_info.bin", "rb")
    content = dict(pickle.load(f))
    f.close()
    return content

def put_user_info(name, rollno, gender, programme, branch, section, username, hostel):
    f = open("./data/user_info.bin", "rb")
    content = dict(pickle.load(f))
    f.close()
    content[str(rollno)] = {
        "name" : name,
        "gender" : gender,
        "programme" : programme,
        "branch" : branch,
        "section" : section,
        "username" : username,
        "hostel" : hostel,
        "rollno" : rollno
    }
    f = open("./data/user_info.bin", "wb")
    pickle.dump(content, f)
    f.close()

def get_user_info(rollno):
    f = open("./data/user_info.bin", "rb")
    content = dict(pickle.load(f))
    f.close()
    return content[str(rollno)]

def check_signup(name, rollno, password1, password2, gender, programme, branch, section, username, hostel):
    login_content = get_login_info()
    user_content = get_all_user_info()
    if password1 != password2:
        return [False, "passwords are not same"]
    for i in user_content.keys():
        if user_content[i]["username"] == username:
            return [False, "username already exists"]
    if rollno in login_content.keys():
        return [False, "password already exists"]
    try:
        put_login_info(rollno, password1)
        put_user_info(name, rollno, gender, programme, branch, section, username, hostel)
        return [True, True]
    except:
        return [False, "error uploading"]

def get_all_posts():
    f = open("./data/posts.bin", "rb")
    l = pickle.load(f)
    f.close()
    return l


def change_rollno_to_username(message):
    f = open("./data/user_info.bin", "rb")
    user_info = dict(pickle.load(f))
    f.close()
    message = list(message.split())
    for i in range(len(message)):
        if message[i][0] == "@":
            rollno = message[i][1:]
            username = user_info[rollno]["username"]
            message[i] = "@" + username
    return_string = ''
    for i in message:
        return_string += i + " "
    return return_string

def get_follow():
    content = dict()
    for i in get_login_info().keys():
        f = open("./data/user_data/{}.bin".format(i), "rb")
        content[i] = list(pickle.load(f))
        f.close()
    return content


def change_username_to_rollno(username):
    f = open("./data/user_info.bin", "rb")
    user_info = dict(pickle.load(f))
    f.close()
    for i in user_info.keys():
        if user_info[i]["username"] == username:
            return i

def push_new_post(message, username):
    message = message.split()
    m = ""
    tag = []
    for i in message:
        if i[0] == "@":
            tag.append(i[1:])
            m += "@" + change_username_to_rollno(i[1:]) + " "
        else:
            m += i + " "
    f = open("./data/posts.bin", "rb")
    content = list(pickle.load(f))
    f.close()
    content.append(["@" + change_username_to_rollno(username), m, tag, str(datetime.datetime.now())[:-7]])
    f = open("./data/posts.bin", "wb")
    pickle.dump(content, f)
    f.close()
