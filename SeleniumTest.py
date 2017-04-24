from selenium import webdriver
import time, requests
from lxml import html
from unittest import TestCase, main

kupindo_url="https://www.kupindo.com/"


def get_actual_prices(url):

    r = requests.get(url)
    tree = html.fromstring(r.content)

    #gets all elements with specific class
    prices_html_elements = tree.xpath("//*[@class='item_price'] ")
    actual_prices = []

    for item in prices_html_elements:

    #gets only decimal values from text string
        all_prices = [s for s in item.text_content().split() if s.decode('utf8').isdecimal()]

    #removes first price from items with discounts

        actual_price = all_prices[-1]

        actual_prices.append(float(actual_price))

    return actual_prices


class TestDylanDog(TestCase):

        def setUp(self):
            self.driver = webdriver.PhantomJS()
            self.driver.set_window_size(1120, 550)

        def test_url(self):
            self.driver.get(kupindo_url)

            #search for Dylan Dog
            self.driver.find_element_by_id('txtPretraga').send_keys("Dylan Dog")
            self.driver.find_element_by_id("search_button").click()
            time.sleep(4)

            #select sorting option Ascending -> Change option[3] to get sorting by Desccending
            self.driver.find_element_by_xpath("//*[@id='container_right']/div[1]/div/select/option[2]").click()

            #Asserts sorted list if Equal
            self.assertListEqual(get_actual_prices(self.driver.current_url), sorted(get_actual_prices(self.driver.current_url)))

        def teaarDown(self):
            self.driver.quit()

if __name__ == '__main__':
    main()