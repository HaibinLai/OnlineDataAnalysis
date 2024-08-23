import re
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service()
options = webdriver.Options()
browser = webdriver.WebDriver(service=service, options=options)

browser.get('https://hotel.bestwehotel.com/HotelSearch/?checkinDate=2024-08-24&checkoutDate=2024-08-25&cityCode'
            '=AR04567&queryWords=&cityName=%E4%B8%8A%E6%B5%B7&extend=1,1,0,0,0,0')


# time.sleep(1)

class Spider(object):
    def __init__(self, city):
        self.city = city
        self.spiderUrl = 'https://hotel.bestwehotel.com/HotelSearch/?cityName=%s'

    def start_spider(self):
        service = Service()
        options = webdriver.Options()
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        browser = webdriver.WebDriver(service=service, options=options)
        return browser

    def init(self):
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["title", "address", "cover", "overCenter", "type", "tag", "start", "price", "description",
                     "houseTypeList", "commentList", "detailLink", "city"])

    def main(self):
        browser = self.start_spider()
        print('Url:', self.spiderUrl % self.city)
        browser.get(self.spiderUrl % self.city)
        # time.sleep(1)
        self.sm(browser)

    def sm(self, browser):
        # double // means  global search on site
        hotel_list = browser.find_elements(by=By.XPATH, value='//div[@class="info"]/div[@class="block ng-scope"]')
        print(hotel_list)

        for hotel in hotel_list:
            # cover jpeg
            cover = hotel.find_element(by=By.XPATH, value='./div[@class="pic"]/a/img').get_attribute("src")
            print(cover)

            # link
            detail_link = hotel.find_element(by=By.XPATH, value='./div[@class="pic"]/a').get_attribute("href")

            # title
            title = hotel.find_element(by=By.XPATH, value='./div[@class="top clearfix"]/p[@class="name"]/a').text

            # address
            address = hotel.find_element(by=By.XPATH,
                                         value='./div[@class="top clearfix"]/p[@class="address ng-binding"]/span').text

            # center
            overCenter = hotel.find_element(by=By.XPATH,
                value='./div[@class="top clearfix"]/p[@class="distance ng-binding ng-scope"]').text

            print(title, address, detail_link, overCenter)

            # star
            star = hotel.find_element(by=By.XPATH,
                value='./div[@class="top clearfix"]/div[@class="rank"]/div[@class="score"]/span').text

            # type
            type = hotel.find_element(by=By.XPATH,
                value ='./div[@class="middle clearfix"]/div[@class="tag ng-binding ng-scope"]').text

            # tag
            try:
                tag = hotel.find_element(by=By.XPATH, value='./div[@class="icon clearfix"]/span')
                tag = ", ".join([x.text for x in tag])
            except:
                tag = ""
            print(star, type, tag)

            # price
            price = hotel.find_element(by=By.XPATH,
                value ='./div[@class="bottom clearfix"]/div/div/span').text
            print(price)

            break


if __name__ == '__main__':
    spiderObj = Spider("北京")
    # spiderObj.init()
    spiderObj.main()
