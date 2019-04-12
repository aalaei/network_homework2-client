# import sys
import os
import requests
import platform

# import json
from sys import stdin

import webbrowser

read = stdin.readline

tok = 0
state = 0


def sign_up():
    print ("Welcome, Please enter username:")
    username = raw_input()
    if str(username) == "":
        return
    print ("well, now please enter password or empty to cancel")
    passwd = raw_input()
    if str(passwd) == "":
        print ("Operation is canceled!")
        return
    parms = {"username": username, "password": passwd}
    uc = geturl("signup")
    res = requests.post(uc, parms).json()
    print (res["message"])


def pars_status(st):
    st = int(st)
    res = ""
    if st == 1:
        res = "in progress"
    elif st == 2:
        res = "close"
    elif st == 0:
        res = "open"
    return res


def tickettostr(tiket):
    out = ""
    try:
        out = out + "ticket# " + str(tiket["ID"]) + "\n"
    except:
        pass
    try:
        out = out + "Send by: " + str(tiket["username"]) + "\n"
    except:
        pass
    try:
        out = out + "date: " + str(tiket["date"]) + "\n"
    except:
        pass
    try:
        out = out + "Status: " + pars_status(tiket["Status"]) + "\n"
    except:
        pass
    try:
        out = out + "subject: " + tiket["subject"] + "\n" + "_______________________" + "\n"
    except:
        pass
    try:
        out = out + "body: " + tiket["body"] + "\n"
    except:
        pass
    try:
        out = out + "$$$$$\n" + "response: " + tiket["response"] + "\n"
    except:
        pass
    finally:
        out = out + "------------------" + "\n"
    return out


def login():
    print ("Please enter username:")
    username = raw_input()
    if str(username) == "":
        return
    print ("well, now please enter password or empty to cancel")
    passwd = raw_input()
    if str(passwd) == "":
        print ("Operation is canceled!")
        return
    parms = {"username": username, "password": passwd}
    uc = geturl("login")
    res = requests.post(uc, parms).json()
    if str(res["code"]) == "202":
        uc = geturl("logout")
        res = requests.post(uc, parms).json()
        if str(res["code"]) != "200":
            print ("please logout and login manually")
            return
        else:
            uc = geturl("login")
            res = requests.post(uc, parms).json()
            print (res["message"])
    else:
        print (res["message"])
    global tok
    tok = res["token"]
    if str(tok) != "0" and int(res['code']) == 200:
        global state
        state = renew_state()


def renew_state():
    if str(tok) == "0":
        return 0
    parms = {"token": tok}
    uc = geturl("getticketmod")
    res = requests.get(uc, parms).json()
    code = res["code"]
    if code == 700:
        return 1
    elif code == 200:
        return 2
    else:
        return 0


def checklogin():
    return tok != 0 and tok != "0"


def sendticket():
    if not checklogin():
        print ("please login first")
        return
    print ('enter subject of new ticket:')
    subj = raw_input()
    print ("enter body:")
    body = raw_input()
    if (subj == "" or body == ""):
        return
    parms = {"token": tok, "subject": subj, "body": body}
    uc = geturl("sendticket")
    res = requests.post(uc, parms).json()
    print (res["message"])


def getticketcli():
    if not checklogin():
        print ("please login first")
        return

    parms = {"token": tok}
    uc = geturl("getticketcli")
    res = requests.get(uc, parms).json()
    mes = res["tickets"]
    print (mes)
    n = int((str(mes).split("-"))[1])

    for i in range(0, n):
        # print ("tiket #%s", i)
        it = res["block " + str(i)]
        print(tickettostr(it))


def closeticketcli():
    if not checklogin():
        print ("please login first")
        return
    print ('enter id of the ticket:')
    id = int(raw_input())
    if id == "":
        return
    parms = {"token": tok, "id": id}
    uc = geturl("closeticket")
    res = requests.post(uc, parms).json()
    print (res["message"])


def get_ticketadmin():
    if not checklogin():
        print ("please login first")
        return
    if state < 2:
        print ("you don't have access to this")
        return
    parms = {"token": tok}
    uc = geturl("getticketmod")
    res = requests.get(uc, parms).json()
    mes = res["tickets"]
    print (mes)
    n = int((str(mes).split("-"))[1])

    for i in range(0, n):
        it = res["block " + str(i)]
        print(tickettostr(it))


def restoticketadmin():
    if not checklogin():
        print ("please login first")
        return
    if state < 2:
        print ("you don't have access to this")
        return
    print ('enter id of the ticket:')
    id = int(raw_input())
    if id == "":
        return
    print ('enter body:')
    body = raw_input()
    if body == "":
        return
    parms = {"token": tok, "id": id, "body": body}
    uc = geturl("restoticketmod")
    res = requests.post(uc, parms).json()
    print (res["message"])


def changestatusadmin():
    if not checklogin():
        print ("please login first")
        return
    if state < 2:
        print ("you don't have access to this")
        return
    print ('enter id of the ticket:')
    id = int(raw_input())
    if id == "":
        return
    print ('enter new status:(in progress/close/open)')
    status = raw_input()
    if status == "" or (status != "in progress" and status != "close" and status != "open"):
        return
    parms = {"token": tok, "id": id, "status": status}
    uc = geturl("changestatus")
    res = requests.post(uc, parms).json()
    print (res["message"])


def show_tickets_list():
    if not checklogin():
        print ("please login first")
        return
    if state < 2:
        print ("you don't have access to this")
        return
    parms = {}
    uc = geturl("showT")
    res = requests.get(uc, parms).json()
    n = res["num"]
    tics = res["tickets"]
    for i in range(0, n):
        print (tickettostr(tics[i]))


def changerole():
    if not checklogin():
        print ("please login first")
        return
    if state < 2:
        print ("you don't have access to this")
        return
    print ('enter username of the specified user:')
    username = raw_input()
    if username == "":
        return
    print ('enter new role(A/U):')
    role = raw_input()
    if role == "":
        return
    while role != "A" and role != "U":
        print ('enter new role(A/U):')
        role = raw_input()

    parms = {"token": tok, "username": username, "role": role}
    uc = geturl("changerole")
    res = requests.post(uc, parms).json()
    print (res["message"])


def logout():
    print ("logging out, enter username:")
    username = raw_input()
    if str(username) == "":
        return
    print ("password or empty to cancel")
    passwd = raw_input()
    if str(passwd) == "":
        print ("Operation is canceled!")
        return
    parms = {"username": username, "password": passwd}
    uc = geturl("logout")
    res = requests.post(uc, parms).json()
    print (res["message"])
    global tok
    global state
    tok = 0
    state = 0


def see_help():
    webbrowser.open(geturl(""), new=2)


def usertostr(usr):
    out = "user# "
    try:
        out = out + str(usr["ID"]) + "\n"
    except:
        out = out + "\n"
    try:
        out = out + "Username: " + usr["username"] + "\n"
    except:
        pass
    try:
        out = out + "First Name: " + usr["firstname"] + "\n"
        out = out + "Last Name: " + usr["lastname"] + "\n"
    except:
        pass
    try:
        out = out + "role: " + usr["role"] + "\n"
    except:
        pass
    out = out + "\n-------------------------------\n"
    return out


def show_users_list():
    parms = {}
    uc = geturl("show")
    res = requests.get(uc, parms).json()
    n = res["num"]
    usrs = res["users"]
    for i in range(0, n):
        print(usertostr(usrs[i]))


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def clear_all():
    if not checklogin():
        print ("please login first")
        return
    if state < 2:
        print ("you don't have access to this")
        return
    print ("are you sure?(y/n)")
    i = raw_input()
    while i != "y" and i != "n":
        print ("(y/n)?")
        i = raw_input()
    if i == "n":
        return

    print ('enter password for double check:')
    passwd = str(raw_input())
    parms = {"token": tok, "password": passwd}
    uc = geturl("renumberate")
    res = requests.post(uc, parms).json()
    print (res["message"])
    if str(res['code']) == "200":
        global state
        state = 0


host = "127.0.0.1"
port = 8888


def geturl(comd):
    return "http://" + host + ":" + str(port) + "/" + comd + "?"


if __name__ == "__main__":

    '''switcher = {
        1: sign_up,
        2: login,
        3: sendticket,
        4: getticketcli,
        5: closeticketcli,
        6: get_ticketadmin,
        7: restoticketadmin,
        8: changestatusadmin,
        9: changerole,
        10: logout,
        11: see_help,
        12: show_users_list,
        13: show_tickets_list,
        14: clear_all,
        0: exit
    }'''
    switcher_ = {}
    switcher_[0] = {
        1: sign_up,
        2: login,
        3: see_help,
        4: show_users_list,
        5: logout,
        0: exit
    }
    switcher_[1] = {
        1: show_users_list,
        2: getticketcli,
        3: sendticket,
        4: closeticketcli,
        5: logout,
        6: see_help,
        0: exit
    }
    switcher_[2] = {

        1: show_users_list,
        2: sendticket,
        3: get_ticketadmin,
        4: restoticketadmin,
        5: changestatusadmin,
        6: changerole,
        7: logout,
        8: see_help,
        9: clear_all,
        10: show_tickets_list,
        0: exit
    }
    exe = switcher_[0]
    tok = 0
    on = True
    while on:

        if tok == 0 or tok == "0":
            state = 0
        clear()
        print("Choose your action")
        if state == 0:
            print ("1)sign up \n2)login \n3)see help in browser\n4)show list of users"
                   "\n5)logout\n0)exit")
        elif state == 1:
            print ("1)show list of users\n2)get tickets(user)\n3)sendticket\n4)close ticket(user)"
                   "\n5)logout\n6)see help in browser\n0)exit")

        elif state == 2:

            print ("1)show list of users\n2)sendticket\n3)get tickets(admin)"
                   "\n4)response to ticket(admin)\n5)change status(admin)"
                   "\n6)change user role\n7)logout\n8)see help in browser\n9)clear all of the db\n10)show tickets list\n0)exit")
        try:
            usr_input = read()
        except:
            print ("not able to read")
            usr_input = exit

        try:
            exe = (switcher_[state])[int(usr_input[:-1])]
            clear()
        except:
            "syntax error\n"
        finally:
            pass

        try:
            if exe == exit:
                on = 0
            else:
                exe()
                print ("Press any key to continue...")
                a = stdin.read(1)
        except:
            print ("eee")
        finally:
            pass
