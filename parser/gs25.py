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
from parsed_data.models import ProductGS25
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
    driver_path = str('./chromedriver_mac')
elif osname == "Windows":
    driver_path = str('./chromedriver.exe')
elif osname == "Linux":
    driver_path = str('./chromedriver_linux')
else:
    print("driver selection error ")
print("Driver =>" + driver_path)

driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver.implicitly_wait(3)


def gs25_parser():
    driver.get('http://gs25.gsretail.com/gscvs/ko/products/event-goods')
    driver.find_element_by_xpath('//*[@id="TOTAL"]').click()
    num = 1
    page = 1
    while 1:
        prod_input = []
        try:
            prod_input.append(driver.find_element_by_css_selector(
                '#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(9) > ul > li:nth-child(%s) > div > p.tit' % num).text)  # prod Name
            prod_input.append(driver.find_element_by_css_selector(
                '#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(9) > ul > li:nth-child(%s) > div > p.price > span' % num).text)  # price
            try:
                prod_input.append(driver.find_element_by_css_selector(
                    '#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(9) > ul > li:nth-child(%s) > div > p.img > img' % num).get_attribute(
                    'src'))
            except NoSuchElementException:
                pass
            prod_input.append(driver.find_element_by_css_selector(
                '#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(9) > ul > li:nth-child(%s) > div > div > p > span' % num).text)
            prod_input[1] = prod_input[1].replace(',', '')
            prod_input[1] = prod_input[1].replace('원', '')
            ProductGS25(prodName=prod_input[0], prodPrice=prod_input[1], prodImg=prod_input[2], prodEventType=prod_input[3]).save()
            print(prod_input)
            print(num)
            print(page)
            num += 1
            if num == 9:
                page += 1
                num = 1
                driver.execute_script("goodsPageController.movePage(%d);" % page)
                try:
                    if '검색된 상품이 없습니다.' in (
                    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div[4]/ul/li/p').text):
                        print("Parse END")
                        break
                except NoSuchElementException:
                    print("TTTT")
                    continue
        except NoSuchElementException:
            print("Parse END")
            print("NoSuchElements")
            break
        except StaleElementReferenceException:
            print("Stale")
            time.sleep(1)
