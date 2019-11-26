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
from parsed_data.models import ProductEmart24
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

def emart_parser():
    driver.get('https://www.emart24.co.kr/product/eventProduct.asp')
    num = 1
    col = 0
    prod_list = []
    while 1:
        try:
            while num < 16:
                prod_input = []
                print("emart parsing")
                print(num)
                prod_input.append(driver.find_element_by_css_selector(
                    '#regForm > div.section > div.eventProduct > div.tabContArea > ul > li:nth-child(%s) > div > p.productDiv' % num).text)
                prod_input.append(driver.find_element_by_css_selector(
                    '#regForm > div.section > div.eventProduct > div.tabContArea > ul > li:nth-child(%s) > div > p.price' % num).text)
                try:
                    prod_input.append(driver.find_element_by_css_selector(
                        '#regForm > div.section > div.eventProduct > div.tabContArea > ul > li:nth-child(%s) > div > p.productImg' % num).find_element_by_tag_name(
                        'img').get_attribute('src'))
                except NoSuchElementException:
                    pass

                prod_input[1] = prod_input[1].replace(',', '')
                prod_input[1] = prod_input[1].replace(' 원', '')

                if '→' in prod_input[1]:
                    prod_input[1] = prod_input[1].replace('→ ', '')
                    prod_input[1] = prod_input[1].split(' ')[1]

                eventtype = driver.find_element_by_xpath(
                    '//*[@id="regForm"]/div[2]/div[3]/div[2]/ul/li[%s]/div/div/p/img' % num).get_attribute('alt')
                if '2 + 1 뱃지' in eventtype:
                    eventtype = '2+1'
                elif 'SALE 뱃지' in eventtype:
                    eventtype = 'sale'
                elif 'X2 더블 뱃지' in eventtype:
                    eventtype = 'dum'
                elif '1 + 1 뱃지 이미지' in eventtype:
                    eventtype = '1+1'
                elif '3 + 1 뱃지' in eventtype:
                    eventtype = '3+1'
                else:
                    eventtype = 'error!'
                prod_input.append(eventtype)
                ProductEmart24(prodName=prod_input[0], prodPrice=prod_input[1], prodImg=prod_input[2],
                                prodEventType=prod_input[3]).save()
                num += 1
                if num is 16:
                    col += 1
                    num = 1
                    driver.find_element_by_css_selector(
                        '#regForm > div.section > div.eventProduct > div.paging > a.next.bgNone').click()
        except NoSuchElementException:
            print("파싱종료")
            break
        except StaleElementReferenceException:
            time.sleep(0.5)
        except ElementClickInterceptedException:
            time.sleep(1)