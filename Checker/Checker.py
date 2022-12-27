from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time,random,string,os

def rs(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://192.168.1.52:8321/")

user,passwd = rs(10),rs(10)
username = user
password = passwd
print (username,password)

def register ():
    driver.find_element_by_class_name("button_adv").click()
    driver.implicitly_wait (10)

    driver.find_element_by_id("uname").send_keys(username)
    driver.find_element_by_id("passwd").send_keys(password)
    driver.find_element_by_id("makereg").click()
    print ("register success")
    time.sleep (2)

    alert = driver.switch_to_alert()
    alert.accept()
    print ("alert accept")
    driver.implicitly_wait (10)

    driver.find_element_by_class_name ("close").click ()
    driver.implicitly_wait (10)
register()


def login ():
    driver.find_element_by_class_name ("login_account").click()
    print (username,password)
    driver.implicitly_wait (10)

    driver.find_element_by_id("uname1").send_keys(username)
    driver.find_element_by_id("passwd1").send_keys(password)
    driver.find_element_by_id("makelog").click()
    print ('login success')
    time.sleep (2)

    alert = driver.switch_to_alert()
    alert.accept()
    print ("alert accept")
    driver.implicitly_wait (10)

    driver.find_element_by_link_text ("Close the window").click ()
    driver.implicitly_wait (10)
login ()

def converter ():
    driver.find_element_by_name ("user_video").send_keys(os.getcwd()+"/ifmo.mp4")
    time.sleep (3)
    driver.find_element_by_name ("start_time").send_keys(0)
    driver.find_element_by_name("duration").send_keys(15)
    driver.find_element_by_xpath ('//*[@value = "Convert"]').click ()
    time.sleep (5)
    alert = driver.switch_to_alert()
    alert.accept()
    print ("Alert accept\n Video uploaded")
converter ()

time.sleep(10)

def last_check ():
    res = driver.find_element_by_css_selector ("tbody a")
    if res:
        res.click ()
        time.sleep(3)
        print ("Congratulations! Site worked without any errors")
last_check ()

time.sleep(5)
driver.close() 