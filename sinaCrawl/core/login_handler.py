# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginHandler(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        options = webdriver.ChromeOptions()
        options.set_headless(headless=True)
        self.driver = webdriver.Chrome(options=options)
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/'
        self.wait = WebDriverWait(self.driver, 5)

    def open(self):
        self.driver.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def run(self):
        try:
            self.open()
            WebDriverWait(self.driver, 30).until(EC.title_is('我的首页'))
            cookies = self.driver.get_cookies()
            cookie = [item["name"] + "=" + item["value"] for item in cookies]
            cookie_str = '; '.join(item for item in cookie)
            self.driver.quit()
            return cookie_str
        except Exception:
            return ''


if __name__ == '__main__':
    cookie = LoginHandler('18355094977', 'LOL19960921').run()
    print(cookie)

