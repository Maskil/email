import datetime
import json
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.mime.application
from email.mime.application import MIMEApplication
from os.path import basename
import requests
import os

apikey = 'o1zO8aOonyH3VdhZtmWEvBCXy2dkGSe0'  # https://developer.nytimes.com/ here to get your API, but I think this is available.

def add():
    label = {readN()['results'][0]['abstract']}
    notes['abstract'] = label
    print(article)
    writeF()


def ynAnswer(question):
    userAns = input(question)
    while (not (userAns == "Y" or userAns == "y" or userAns == "N" or userAns == "n")):
        print('Please input either Y or N.')
        userAns = input(question)
    return userAns


def addC():
    readC()
    print('You are adding a contact.')
    name = input('Type the name of the person you are adding: ')
    if name in contacts:
        print('%s already exists in your contacts.' % name)
        return 0
    else:
        email = (input('Type their email address: '))
        for key, value in contacts.items():
            if email == value['email address']:
                print('email exists. His/Her username is: ' + key)
                return 0
        label = {'email address': email}
        contacts[name.lower()] = label
        writeC()


def writeC():
    js = json.dumps(contacts)
    file = open('contacts.txt', 'w')
    file.write(js)
    file.close()


def readC():
    global contacts
    try:
        file = open('contacts.txt', 'r')
        contacts = {}
        js = file.read()
        contacts = json.loads(js)
        file.close()
    except:
        file = open('contacts.txt', 'a')


def writeS():
    js = json.dumps(signature)
    file = open('signature.txt', 'w')
    file.write(js)
    file.close()


def readS():
    global signature
    try:
        file = open('signature.txt', 'r')
        signature = {}
        js = file.read()
        signature = json.loads(js)
        file.close()
    except:
        file = open('signature.txt', 'a')


def addS():
    print('Write your signature. Type 1q1q to stop:' + '\n')
    signature[username] = {}
    global numS
    numS = 0
    while (True):
        text = str(input())
        if (text == "1q1q"):
            print('Body ended.')
            break
        signature[username][numS] = text
        numS += 1
    writeS()


def writeF():
    js = json.dumps(notes)
    file = open('usernames.txt', 'w')
    file.write(js)
    file.close()


def readF():
    global notes
    try:
        file = open('usernames.txt', 'r')
        notes = {}
        js = file.read()
        notes = json.loads(js)
        file.close()
    except:
        file = open('usernames.txt', 'a')
        notes = {}


def writeA():
    js = json.dumps(article)
    file = open('news.txt', 'w')
    file.write(js)
    file.close()


def readA():
    global article
    try:
        file = open('news.txt', 'r')
        article = {}
        js = file.read()
        article = json.loads(js)
        file.close()
    except:
        file = open('news.txt', 'a')
        article = {}


def writeG():
    js = json.dumps(groups)
    file = open('groups.txt', 'w')
    file.write(js)
    file.close()


def readG():
    global groups
    try:
        file = open('groups.txt', 'r')
        groups = {}
        js = file.read()
        groups = json.loads(js)
        file.close()
    except:
        file = open('groups.txt', 'a')
        groups = {}


def readN(num):
    global section
    section = {1: 'world', 2: 'us', 3: 'business', 4: 'technology', 5: 'science', 6: 'health', 7: 'sports',
               8: 'opinion', 9: 'arts', 10: 'style', 11: 'travel', 12: 'jobs'}
    query_url = f"https://api.nytimes.com/svc/topstories/v2/{section[num]}.json?api-key={apikey}"
    r = requests.get(query_url)
    # pprint(r.json())
    tmp = serialize_sets(r.json())
    for i in range(5):
        label = {"title": tmp['results'][i]['title'], "abstract": tmp['results'][i]['abstract'],
                 "url": tmp['results'][i]['url']}
        article['news' + str(i)] = label
        writeA()


def makeGroup():
    readC()
    print('You are adding a group.')
    numMember = intAnswer('How many people do you want in this group? Answer in numbers: ')
    group = {}
    groupName = input('Write a name for your group: ')
    for i in range(0, numMember):
        while True:
            try:
                name = input('Write the name of person #' + str(i + 1) + ": ")
                if name.lower() in contacts:
                    group[name.lower()] = contacts[name.lower()]
                    break
                else:
                    print('The name inputted is not included in your contacts.')
                    addC()
            except ValueError:
                print('Please re-input.')
    groups[groupName.lower()] = group
    writeG()
    print("Group %s has been successfully created." % groupName)


def deleGroup():
    print(groups.items())
    groupName = (input('Write the name of the group you are deleting: '))
    if groupName in groups:
        del groups[groupName]
        print("%s" % groups.items())
        writeG()
    else:
        print('%s was not found in your groups.' % groupName)


def menu():
    print('''
    1. World
    2. U.S
    3. Business
    4. Technology
    5. Science
    6. Health
    7. Sports
    8. Opinion
    9. Arts
    10: Style
    11: Travel
    12: Jobs
    ''')
    return int(input("What kind of news do you like? Answer in numbers.\n"))


def intAnswer(question):
    userAns = input(question)
    while (not userAns.isdigit()):
        print('Please input an integer value.')
        userAns = input(question)
    return int(userAns)


def delU():
    useranme = input("The username you want to delete: ")
    if useranme in notes:
        del notes[useranme]
        print("%s" % notes.items())
        writeF()
    else:
        print('%s was not found.' % useranme)


def add_username():
    readF()
    print('You are adding a username.')
    name = input('Type your username: ')
    if name in notes:
        print('username exists')
        return 0
    email = (input('Type your email address: '))
    for key, value in notes.items():
        if email == value['email']:
            print('email exists. Your username is: ' + key)
            return 0
    psw = input('Write your password: ')
    label = {'email': email, 'password': psw}
    notes[name.lower()] = label
    writeF()


def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj


readF()
readA()
readC()
readS()
def mail():
    print('Connecting to server...')
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)  # or 465.
    smtpObj.ehlo()  # setup.
    smtpObj.starttls()  # encryption.
    while True:
        try:
            readF()
            global username
            username = input('Please enter your username: ').lower()
            smtpObj.login(notes[username]['email'], notes[username]['password'])
            break
        except:
            print("go to https://myaccount.google.com/u/3/security or username not found.")
            add_username()
    print("logged in")
    msg = MIMEMultipart()
    subject = input("Your subject: ")
    msg['Subject'] = subject
    msg['From'] = 'EMAIL@gmail.com'
    answer = input('Sending to group: Y. Inputting all recipients: N. ')
    if answer == 'Y' or answer=='y':
        readG()
        while True:
            if len(groups) == 0:
                print('No groups found. Creating a new group.')
                makeGroup()
            elif len(groups)>0:
                break
        recipientList = []
        for groupName in groups:
            print(groupName.capitalize())
        while True:
            try:
                sendTo = input('Write the group name of the group you want to send your email to: ')
                if sendTo.lower() in groups:
                    for name in groups[sendTo.lower()]:
                        recipientList.append(groups[sendTo.lower()][name.lower()]['email address'])
                    break
                else:
                    answer = input('The group name inputted is not included in your groups. Do you want to make a new group? Y/N')
                    if answer=='Y' or answer=='y':
                        makeGroup()
            except ValueError:
                print('Please re-input')
    else:
        recipientList = []
        numRecipient = intAnswer('How many recipients? Answer in numbers: ')
        i = 0
        print('Type c to enter name or e to enter email address: ')
        while i < numRecipient:
            tyPe = input('#' + str(i + 1) + 'type: ')
            if tyPe == 'c':
                flag = True
                while flag:
                    try:
                        readC()
                        rc = input('Please insert the name of the recipient: ').lower()
                        recipientList.append(contacts[rc]['email address'])
                        flag = False
                    except:
                        print("Contact not found.")
                        addC()
            elif tyPe == 'e':
                while True:
                    try:
                        recipientList.append(input('Please insert the email address of the recipient: '))
                        break;
                    except:
                        print('Invalid address; please redo.')
            else:
                continue
            i += 1
    print("Please start typing your body.")
    text = ''
    while (True):
        text = str(input())
        if (text == "1q1q"):
            print('Body ended.')
            break
        if (text == "news"):
            readA()
            text = ""
            body3 = MIMEText('\n')
            answer = menu()
            readN(answer)
            body = f"""\
                <html>
                    <head></head>
                    <body>
                        <p>News section: <b><u>{section[answer]}</u></b><br>
                        <br>
                        </p>
                    </body>
                </html>
                """
            category_body = MIMEText(body, 'html')
            msg.attach(category_body)
            i = 1
            for key, value in article.items():
                newsBody1 = f"""\
                <html>
                    <head></head>
                    <body>
                        <p><b>{str(i) + '. '}{value['title']}</b><br>
                        </p>
                    </body>
                </html>
                """
                body = MIMEText(newsBody1, 'html')
                msg.attach(body)
                # newsBody = value['title'] + '\n' + value['abstract'] + '\n' + '\n'
                newsBody = value['abstract'] + '\n' + 'Learn more: ' + value['url'] + '\n'
                body = MIMEText(newsBody)
                msg.attach(body)
                msg.attach(body3)
                i += 1
            article.clear()
            body = MIMEText('--------------------------------------------------------')
            msg.attach(body)
        body2 = MIMEText(text + '\n')
        msg.attach(body2)
    answer = input('Do you want to insert a signature? Y or N: ')
    if (answer == "Y" or answer == "y"):
        readS()
        i = 0
        text = MIMEText('\n')
        msg.attach(text)
        msg.attach(text)
        print('This is your current signature.\n')
        try:
            i = 0
            while i < len(signature[username]):
                print(signature[username][str(i)])
                i += 1
        except:
            print("No any signature yet.")
        print('----------------------------------')
        answer = input('Do you want to change your signature? Y or N: ')
        if (answer == "Y" or answer == "y"):
            addS()
        i = 0
        while i < len(signature[username]):
            readS()
            text = MIMEText(signature[username][str(i)])
            msg.attach(text)
            text = MIMEText('\n')
            msg.attach(text)
            i += 1
    answer = input('Would you like to attach a file? Type Y for Yes and N for No.\n')
    if (answer == 'Y' or answer=='y'):
        print('Type your file location. Type 1q1q to stop.')
        while True:
            location = str(input())
            if location == '1q1q':
                break
            with open(location, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(location)
                )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(location)
            msg.attach(part)
        print('Successfully created all attachments.')
    print("waiting to send")
    while True:
        answer = input("Y: Send Now.\nT: set a time\nR: set a duration for repeating")
        if answer == "Y" or answer == "y":
            smtpObj.sendmail('EMAIL@gmail.com', recipientList, msg.as_string())
            smtpObj.quit()
            print("sent")
            break
        elif answer == "T" or answer == "t":
            hour = input("hour: ")
            minute = input("minute: ")
            second = input("second: ")
            now_time = datetime.datetime.now()
            next_year = now_time.date().year
            next_month = now_time.date().month
            next_day = now_time.date().day
            next_time = datetime.datetime.strptime(
                str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " " + hour + ":" + minute + ":" + second,
                "%Y-%m-%d %H:%M:%S")
            timer_start_time = (next_time - now_time).total_seconds()
            print(str(round(timer_start_time/3600, 2)) + " hours left.")
            print("target: " + str(next_time))
            if timer_start_time > 0:
                time.sleep(timer_start_time)
                smtpObj.sendmail('EMAIL@gmail.com', recipientList, msg.as_string())
                smtpObj.quit()
                break
            else:
                continue
        elif answer == 'R' or answer == 'r':
            print('Answer in integers')
            hour = int(input('hour: '))
            minute = int(input('minute: '))
            print('Command received. Do not close the window.')
            while True:
                time.sleep(hour * 3600 + minute * 60)
                smtpObj.sendmail('EMAIL@gmail.com', recipientList, msg.as_string())
                print('Sent')
        else:
            continue


dirct = os.getcwd()
print('Your current directory is: ' + str(dirct))
qs = ynAnswer('Do you want to change your directory address? Y/N.\n')
if qs == 'Y':
    sure = 'N'
    while sure != 'Y':
        dirct = input('New directory address: ')
        sure = ynAnswer('Are you sure? Please type Y or N. ')
os.chdir(dirct)
d = dirct + '/'
print(f"New directory {os.getcwd()} set")
mail()
