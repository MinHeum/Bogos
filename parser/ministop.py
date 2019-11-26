# -*- coding: utf-8 -*-

from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bogo.settings')
import django
django.setup()
from parsed_data.models import ProductMiniStop
import platform
import os

os.chmod('./chromedriver_mac', 777)
os.chmod('./chromedriver_linux', 777)
os.chmod('./chromedriver.exe', 777)
driver_path = ''
osname = platform.system()
print("OS=>" + osname)

# Chrome 창을 띄우지 않고(headless 하게) driver 를 사용하기 위한 options 변수 선언 및 설정 그리고 driver 선언
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("--disable-gpu")
if osname == "Darwin":
    driver_path= str('./chromedriver_mac')
elif osname == "Windows":
    driver_path = str('./chromedriver.exe')
elif osname == "Linux":
    driver_path = str('./chromedriver_linux')
else:
    print("driver selection error ")
print("Driver =>" + driver_path)

driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver.implicitly_wait(3)

def ministop_parser():
    driver.get('https://www.ministop.co.kr/MiniStopHomePage/page/event/plus1.do')
    # 전부 불러오기! [1+1]
    num = 1
    while 1:
        try:
            driver.find_element_by_css_selector(
                '#section > div.inner.wrap.service1 > div.event_plus_list > div > a.pr_more').click()
            time.sleep(0.3)
        except NoSuchElementException:
            print("출력 끝...")
            break
    while 1:
        try:
            prod_input = []
            prod_input.append(driver.find_element_by_css_selector(
                '#section > div.inner.wrap.service1 > div.event_plus_list > ul > li:nth-child(%) > a > p').text)
            prod_input = prod_input[0].split('\n')
            try:
                prod_input.append(driver.find_element_by_css_selector(driver.find_element_by_css_selector(
                    '#section > div.inner.wrap.service1 > div.event_plus_list > ul > li:nth-child(%s) > a' % num).find_element_by_tag_name(
                    'img').get_attribute('src')))
            except NoSuchElementException:
                pass
            prod_input.append("1+1")
            ProductMiniStop(prodName=prod_input[0], prodPrice=prod_input[1], prodImg=prod_input[2], prodEventType=prod_input[3]).save()
            num += 1
        except NoSuchElementException:
            break
    # 전부 불러오기! [2+1]
    driver.get('https://www.ministop.co.kr/MiniStopHomePage/page/event/plus2.do')
    num = 1
    while 1:
        try:
            driver.find_element_by_css_selector(
                '#section > div.inner.wrap.service1 > div.event_plus_list > div > a.pr_more').click()
            time.sleep(0.3)
        except NoSuchElementException:
            print("출력 끝...")
            break
    while 1:
        try:
            prod_input = []
            prod_input.append(driver.find_element_by_css_selector(
                '#section > div.inner.wrap.service1 > div.event_plus_list > ul > li:nth-child(%) > a > p').text)
            prod_input = prod_input[0].split('\n')
            try:
                prod_input.append(driver.find_element_by_css_selector(driver.find_element_by_css_selector(
                    '#section > div.inner.wrap.service1 > div.event_plus_list > ul > li:nth-child(%s) > a' % num).find_element_by_tag_name(
                    'img').get_attribute('src')))
            except NoSuchElementException:
                pass
            prod_input.append("2+1")
            ProductMiniStop(prodName=prod_input[0], prodPrice=prod_input[1], prodImg=prod_input[2], prodEventType=prod_input[3]).save()
            num += 1
        except NoSuchElementException:
            break
