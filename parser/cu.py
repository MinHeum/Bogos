# -*- coding: utf-8 -*-

from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bogo.settings')
import django
django.setup()
from parsed_data.models import ProductCU
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


def cu_parser():
    driver.get('http://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N')
    while 1:
        try:
            driver.find_element_by_css_selector(
                '#contents > div.relCon > div.prodListWrap > div > div.prodListBtn-w > a').click()
            time.sleep(0.5)
        # ElementClickInterceptedException Exception 이 발생하면 1초 대기한다.
        except ElementClickInterceptedException:
            time.sleep(1)
        except StaleElementReferenceException:
            time.sleep(1)
        # NoSuchElementException 이 발생하면 더 이상 불러올 상품이 없다는 뜻이니 페이지 LOAD 를 중단한다.
        except NoSuchElementException:
            print("CU Parsing END")
            break

    # 순서대로 파싱하기위한 변수 선언
    num = 17
    col = 1
    prod_list = []
    while 1:
        prod_input = []
        try:
            print(str(int(num / 17) * 40 + col - 40) + "번째 상품")
            # 상품의 이름 및 가격 (line1: name, line2: price)
            prod_input.append(driver.find_element_by_css_selector(
                '#contents > div.relCon > div.prodListWrap > ul:nth-child(%s) > li:nth-child(%s) > p.prodName' % (
                    num, col)).text)
            prod_input.append(driver.find_element_by_css_selector(
                '#contents > div.relCon > div.prodListWrap > ul:nth-child(%s) > li:nth-child(%s) > p.prodPrice' % (
                    num, col)).text)
            prod_input.append(driver.find_element_by_css_selector(
                '#contents > div.relCon > div.prodListWrap > ul:nth-child(%s) > li:nth-child(%s) > div > a' % (
                    num, col)).find_element_by_tag_name('img').get_attribute('src'))
            prod_input.append(driver.find_element_by_css_selector(
                "#contents > div.relCon > div.prodListWrap > ul:nth-child(%s) > li:nth-child(%s) > ul > li" % (
                    num, col)).text)
            col += 1
            if col is 40:
                col = 1
                num += 17
            prod_input[1] = prod_input[1].replace(',', '')
            prod_input[1] = prod_input[1].replace('원', '')
        except NoSuchElementException:
            print("CU Append successfully done.")
            break
        ProductCU(prodName=prod_input[0], prodPrice=prod_input[1], prodImg=prod_input[2], prodEventType=prod_input[3]).save()
