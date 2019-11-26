# -*- coding: utf-8 -*-

from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bogo.settings')
import django
django.setup()
from parsed_data.models import ProductSevenvEleven
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

def seven_parser():
    '''
    세븐일레븐 크롤러
    '''
    driver.get('http://www.7-eleven.co.kr/product/presentList.asp')
    # 전부 불러오기!
    while 1:
        try:
            # driver.find_element_by_xpath('//*[@id="listUl"]/li[15]/a/span').click()
            driver.find_element_by_class_name("btn_more").click()
            time.sleep(2)
        except ElementNotInteractableException:
            print("line282")
            break
        except NoSuchElementException:
            print("line285 : 불러오기 완료.")
            break
        except ElementClickInterceptedException:
            pass
    driver.implicitly_wait(1)

    num = 2
    while 1:
        prod_input = []
        try:
            if num <= 14:
                prod_input.append(driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div' % num).text)
                prod_input.append(driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div/div/div[2]' % num).text)
                prod_input.append(
                    driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div' % num).find_element_by_tag_name(
                        'img').get_attribute('src'))
                prod_input.append("1+1")
            else:
                prod_input.append(driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div/div' % num).text)
                prod_input.append(
                    driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div/div/div/div[2]' % num).text)
                prod_input.append(
                    driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div/div' % num).find_element_by_tag_name(
                        'img').get_attribute('src'))
                prod_input.append("1+1")
            prod_input[1] = prod_input[1].replace(',', '')
            print("2+1중에" + str(num) + "번째 상품 넣는중")
            ProductSevenvEleven(prodName=prod_input[0], prodPrice=prod_input[1], prodImg=prod_input[2],
                                prodEventType=prod_input[3]).save()
            num += 1
        except NoSuchElementException:
            print("line312:NoSuchElementException, NUN :" + str(num))
            break
        except StaleElementReferenceException:
            print("line303")
            break
    # 2+1 상품으로 넘어가기
    driver.execute_script('javascript: fncTab(2)')
    time.sleep(2)
    # 전부 불러오기!
    while 1:
        try:
            driver.find_element_by_class_name("btn_more").click()
            time.sleep(1)
        except NoSuchElementException:
            print("line312:More Ended...")
            break
        except StaleElementReferenceException:
            print("line319")
            break
        except ElementClickInterceptedException:
            pass

    num = 2
    while 1:
        prod_input = []
        try:
            if num <= 14:
                prod_input.append(driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div/div/div[1]' % num).text)
                prod_input.append(
                    driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div/div/div[2]' % num).text)
                prod_input.append(
                    driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div' % num).find_element_by_tag_name(
                        'img').get_attribute('src'))
            else:
                prod_input.append(
                    driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div/div/div/div[1]' % num).text)
                prod_input.append(
                    driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div/div/div/div[2]' % num).text)
                prod_input.append(
                    driver.find_element_by_xpath('//*[@id="listUl"]/li[%s]/div/div' % num).find_element_by_tag_name(
                        'img').get_attribute('src'))

            prod_input.append("2+1")
            prod_input[1] = prod_input[1].replace(',', '')
            print("2+1중에" + str(num) + "번째 상품 넣는중")
            ProductSevenvEleven(prodName=prod_input[0], prodPrice=prod_input[1], prodImg=prod_input[2],
                                prodEventType=prod_input[3]).save()
            num += 1
        except NoSuchElementException:
            print("parsing done")
            break
        except StaleElementReferenceException:
            print("StaleElementReferenceException")
            break
