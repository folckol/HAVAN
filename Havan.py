# Product by Rescue Alpha
#
# Discord:
# https://discord.gg/438gwCx5hw
#
# Telegram:
# https://t.me/rescue_alpha

import json
import os
import time

import zipfile
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait

dd = []
with open('data.txt', 'r') as file:
    for i in file:
        dd.append(i.strip('\n'))

api_key = dd[0]


def using_proxy():
    def get_proxy():
        proxy = {}

        with open("proxy.txt", "r") as file:
            proxy = file.readline()
            file.close()

        return proxy

    proxy = str(get_proxy())
    proxy_list = proxy.split(':')
    pass1 = str(proxy_list[3])

    PROXY_HOST = str(proxy_list[0])  # rotating proxy or host
    PROXY_PORT = str(proxy_list[1])
    PROXY_USER = str(proxy_list[2])
    PROXY_PASS = str(pass1.strip())

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "browsingData",
            "proxy",
            "storage",
            "tabs",
            "webRequest",
            "webRequestBlocking",
            "downloads",
            "notifications",
            "<all_urls>"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    return manifest_json, background_js, proxy


def acp_api_send_request(driver, message_type, data={}):
    message = {
        # всегда указывается именно этот получатель API сообщения
        'receiver': 'antiCaptchaPlugin',
        # тип запроса, например setOptions
        'type': message_type,
        # мерджим с дополнительными данными
        **data
    }
    # выполняем JS код на странице
    # а именно отправляем сообщение стандартным методом window.postMessage
    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))


def get_chromedriver(use_proxy=True, user_agent=UserAgent):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()

    proxy = ''

    if use_proxy and dd[1] == 'Y':
        manifest_json, background_js, proxy = using_proxy()

        pluginfile = 'Proxy_ext.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)

        proxy_list = proxy.split(':')

    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)


    chrome_options.add_extension('AntiCaptcha.zip')
    chrome_options.add_extension('Havan_Wallet.crx')


    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    return driver, proxy


def nft():
    driver, proxy = get_chromedriver(use_proxy=True, user_agent=True)

    opts = Options()
    # print(driver.window_handles)
    wait = WebDriverWait(driver, 500)

    time.sleep(5)

    driver.maximize_window()

    while len(driver.window_handles) != 1:
        driver.switch_to.window(driver.window_handles[0])
        driver.close()

    driver.switch_to.window(driver.window_handles[0])

    # Активируем антикапчу
    driver.get('https://antcpt.com/blank.html')
    acp_api_send_request(
        driver,
        'setOptions',
        {'options': {'antiCaptchaApiKey': api_key}}
    )

    time.sleep(5)

    # Регистрируем кошелек

    driver.get('chrome-extension://cnncmdhjacpkmjmkcafchppbnpnhdmon/src/pages/popup/index.html')

    wait.until(element_to_be_clickable((By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/button')))
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/button')).click().perform()

    wait.until(element_to_be_clickable((By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/div[2]/button')))
    ActionChains(driver).move_to_element(
        driver.find_element(By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/div[2]/button')).click().perform()

    wait.until(visibility_of_element_located((By.XPATH, '//*[@id=":r0:"]')))
    driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys('Password123Password123')
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys('Password123Password123').perform()
    time.sleep(1)

    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()

    wait.until(element_to_be_clickable((By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/div/div[2]/div[1]/button')))
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/div/div[2]/div[1]/button')).click().perform()

    wait.until(
        element_to_be_clickable((By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/div[1]/div[2]/button')))
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                             '//*[@id="__root"]/main/div[1]/div/div/section/div[1]/div[2]/button')).click().perform()

    mnemonic = pyperclip.paste()
    time.sleep(1)

    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()
    time.sleep(1)

    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()
    time.sleep(1)

    wait.until(visibility_of_element_located((By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/div/div[2]/button[1]')))

    mnem = driver.find_elements(By.CSS_SELECTOR, 'div.mnemonic--div--group > button.MuiButton-text')

    for i in mnemonic.split(' '):
        for ii in mnem:
            if ii.text == i:
                ii.click()

    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/button').click()

    wait.until(element_to_be_clickable((By.XPATH, '//*[@id=":r2:"]')))
    driver.find_element(By.XPATH, '//*[@id=":r2:"]').send_keys('Account')

    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()
    time.sleep(1)

    wait.until(visibility_of_element_located((By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/div/div[1]/div/div/button')))
    driver.find_element(By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/div/div[1]/div/div/button').click()
    time.sleep(1)

    address = pyperclip.paste()

    time.sleep(1)

    driver.get('https://event.vega.havah.io/')

    wait.until(element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/header/button')))
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH ,'//*[@id="root"]/div/header/button')).click().perform()

    while len(driver.window_handles) == 1:
        pass

    driver.switch_to.window(driver.window_handles[-1])

    wait.until(element_to_be_clickable((By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/div[2]/div[1]/div/label/span[1]/input')))
    driver.find_element(By.XPATH, '//*[@id="__root"]/main/div[1]/div/div/section/div[2]/div[1]/div/label/span[1]/input').click()

    time.sleep(1)

    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()

    while len(driver.window_handles) != 1:
        pass

    driver.switch_to.window(driver.window_handles[0])







    time.sleep(10000)

    # print(tokens)

    time.sleep(2)

    with open("result.txt", "a+") as file:
        file.writelines(f"")

    with open('proxy.txt', 'r') as file:
        lines = file.readlines()

    with open('proxy.txt', 'w') as file:
        lines = file.writelines(lines[1:])

    driver.quit()


def main():
    count = 0
    while True:
        try:

            nft()
            count = 0
        except Exception as e:

            if count >= 5:
                break

            # time.sleep(10000)
            print(e)
            count += 1


if __name__ == '__main__':


    main()
