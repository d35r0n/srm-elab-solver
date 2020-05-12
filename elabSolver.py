from selenium import webdriver
from time import sleep
import pyautogui
from os import listdir
from os.path import isfile, join
from selenium.webdriver.chrome.options import Options
from win32api import GetSystemMetrics

try:
    from login_info import Username, Password
except Exception:
    Username = ""
    Password = ""

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(f"--window-size={GetSystemMetrics(0)}x{GetSystemMetrics(1)}")
driver = webdriver.Chrome()
driver2 = webdriver.Chrome(options=chrome_options)

firstQLoc = ((GetSystemMetrics(0))-480),((GetSystemMetrics(1))-679)
codeLoc = ((GetSystemMetrics(0))-585),((GetSystemMetrics(1))-642)
speedFactor = 10

solutionsPath = "Solutions/"
fileList = [f for f in listdir(solutionsPath) if isfile(join(solutionsPath, f))]
base_url = "https://www.snhrepublic.com/search?q="
codeLinkList = list()
updating = False

def sbx(xpath):
    return driver.find_element_by_xpath(xpath)

def sbx2(xpath):
    return driver2.find_element_by_xpath(xpath)

def correctCredentials():
    try:
        sbx('/html/body/app-root/div/app-login/div/mat-card/div[2]/form/div/p')
        return False
    except Exception:
        return True

def login():
    driver.get('https://care.srmist.edu.in/ncrada/login')
    input("Press Enter once you are done Repositioning the Windows...")
    sbx('//*[@id="mat-input-0"]').send_keys(Username)
    sbx('//*[@id="mat-input-1"]').send_keys(Password)
    sbx('/html/body/app-root/div/app-login/div/mat-card/div[2]/form/button').click()
    sleep(20/speedFactor)
    if not correctCredentials():
        print("Error logging into the Account! Credentials are missing/wrong.")
        print("Please login into your account manually and DO NOT do ANYTHING other than just logging in!")
        input("Press Enter in this Window when you are done.")
    try:
        sbx('/html/body/app-root/div/app-student-home/div/mat-card/div/div/app-student-home-card/mat-card/p').click()
    except Exception:
        input("Press Enter when Course Selection button Apears")
        sbx('/html/body/app-root/div/app-student-home/div/mat-card/div/div/app-student-home-card/mat-card/p').click()
    sleep(20/speedFactor)
    pyautogui.click(firstQLoc)

def changeLanguage(toggle,resetFlag):
    dropDown = sbx('/html/body/app-root/div/app-student-solve/div[2]/app-solve-question/div/div[1]/mat-form-field/div/div[1]/div')
    if "C Language" in dropDown.text and toggle==0:
        resetCode(resetFlag)
        return
    elif "CPP Language" in dropDown.text and toggle==1:
        resetCode(resetFlag)
        return
    else:
        dropDown.click()
    sleep(10/speedFactor)
    if toggle==0:
        sbx('//*[text()="C Language"]').click()
        resetCode(resetFlag)
    elif toggle==1:
        sbx('//*[text()="CPP Language"]').click()
        resetCode(resetFlag)
    else:
        print("Invalid Toggle Provided")

def resetCode(resetFlag):
    if resetFlag==0:
        return
    pyautogui.click(codeLoc)
    sleep(1/speedFactor)
    pyautogui.hotkey("ctrl","a")
    sleep(1/speedFactor)
    pyautogui.press("backspace")
    sleep(1/speedFactor)

def findFile(fileList):
    qname = sbx('/html/body/app-root/div/app-student-solve/div[2]/app-solve-question/div/div[2]/div[1]/div/mat-card/div/div[2]/a[2]').text
    try:
        return fileList.index(qname.replace(":","")+".txt")
    except ValueError:
        if findFileOnline(qname.replace(":",""))=="CodeFound!":
            fileList = [f for f in listdir(solutionsPath) if isfile(join(solutionsPath, f))]
            return fileList.index(qname.replace(":","")+".txt")
        else:
            print(getName().replace("Q. ","Q.") + " : Solution not Found")
            return "404"

def search_question(name):
    driver2.get((base_url+name))

def check_404():
    try:
        sbx2('//*[@id="error"]/div[1]/h2/span[1]')
        return True
    except Exception:
        pass
    return False

def solutionFound():
    try:
        sbx2('//*[@id="blog_posts"]/div/div')
        return False
    except Exception:
        pass
    return True

def findAllPosts():
    n = 1
    nextExists = True
    while nextExists:
        try:
            sbx2(f'//*[@id="blog_posts"]/article[{n}]/div/div[2]/h2/a')
            codeLinkList.append(n)
            n += 1
        except Exception:
            nextExists = False

def codeLinkFinder(n):
    xpath = f'//*[@id="blog_posts"]/article[{n}]/div/div[2]/h2/a'
    return sbx2(xpath)

def saveCodeInFile(filename, code):
    path = "Solutions/"
    filename = filename.replace("\n","")+".txt"
    file = open(path+filename,"w")
    file.write(code)
    file.close()

def findCodeID():
    ID_element = sbx2('//*[@id="single_post"]/article/div[1]/div[3]')
    return ID_element.get_attribute('data-id')

def code():
    code_xpath = f'//*[@id="post_body_{findCodeID()}"]/div/pre'
    return sbx2(code_xpath).text

def findFileOnline(qname):
    search_question(qname)
    if check_404():
        return "CodeNotFound!"
    if not solutionFound():
        return "CodeNotFound!"
    codeLink = codeLinkFinder(1)
    codeLink.click()
    sleep(20/speedFactor)
    saveCodeInFile(qname,code())
    return "CodeFound!"

def enterCode(filename):
    code = open(filename,"r").read()
    if "<iostream>".casefold() in code or "<bits/stdc++.h>".casefold() in code:
        changeLanguage(1,1)
    else:
        changeLanguage(0,1)
    sleep(3/speedFactor)
    pyautogui.click(codeLoc)
    sleep(1/speedFactor)
    pyautogui.typewrite(code)

def getName():
    return sbx('/html/body/app-root/div/app-student-solve/div[2]/app-solve-question/div/div[2]/div[1]/div/mat-card/div/div[2]').text

def evaluateResult():
    sbx('/html/body/app-root/div/app-student-solve/div[2]/app-solve-question/div/div[2]/div[2]/mat-card/div[3]/button[2]').click()
    try:
        sleep(20/speedFactor)
        print(getName().replace("Q. ","Q.") + ": RESULT - " + str(getResult()) + "%")
    except Exception:
        sleep(20/speedFactor)
        print(getName().replace("Q. ","Q.") + ": RESULT - " + str(getResult()) + "%")

def getResult():
    try:
        result = sbx('/html/body/app-root/div/app-student-solve/div[2]/app-solve-question/div/div[2]/div[2]/mat-card/div[4]/a[1]').text
        return int(result.replace("RESULT","").replace("%","").replace("-","").replace(" ",""))
    except Exception:
        sleep(30/speedFactor)
        result = sbx('/html/body/app-root/div/app-student-solve/div[2]/app-solve-question/div/div[2]/div[2]/mat-card/div[4]/a[1]').text
        return int(result.replace("RESULT","").replace("%","").replace("-","").replace(" ",""))

def nextQuestion():
    sbx('/html/body/app-root/div/app-student-solve/div[1]/button[2]').click()
    sleep(20/speedFactor)

def solve(fileList):
    if findFile(fileList)!="404":
        fileList = [f for f in listdir(solutionsPath) if isfile(join(solutionsPath, f))]
        enterCode(solutionsPath+fileList[findFile(fileList)])
        return 1
    return 0

def checkAlreadyDone():
    try:
        code = sbx('/html/body/app-root/div/app-student-solve/div[2]/app-solve-question/div/div[2]/div[2]/mat-card/div[1]/codemirror/div/div[6]/div[1]/div/div/div/div[5]').text
    except Exception:
        sleep(20/speedFactor)
        code = sbx('/html/body/app-root/div/app-student-solve/div[2]/app-solve-question/div/div[2]/div[2]/mat-card/div[1]/codemirror/div/div[6]/div[1]/div/div/div/div[5]').text
    if code.replace(" ","").replace("\n","") == '1#include<stdio.h>2intmain(){3printf("HelloWorld");4return0;5}':
        return False
    elif "<iostream>".casefold() in code or "<bits/stdc++.h>".casefold() in code:
        changeLanguage(1,0)
    else:
        changeLanguage(0,0)
    sleep(3/speedFactor)
    sbx('/html/body/app-root/div/app-student-solve/div[2]/app-solve-question/div/div[2]/div[2]/mat-card/div[3]/button[2]').click()
    sleep(20/speedFactor)
    if getResult()==100:
        print(getName().replace("Q. ","Q.") + " : RESULT - 100%")
        return True
    else:
        return False

def mainCode():
    if solve(fileList)==1:
        evaluateResult()
    nextQuestion()
    sleep(10/speedFactor)

if __name__ == "__main__":
    login()
    for i in range(100):
        if not checkAlreadyDone():
            try:
                mainCode()
            except Exception:
                sleep(20/speedFactor)
                mainCode()
        else:
            nextQuestion()