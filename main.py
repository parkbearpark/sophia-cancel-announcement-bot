import datetime
import os
from os.path import join, dirname
import pprint
import re
import time

import dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from twitter import ManageTwitter


class ScrapeLoyola:
    def __init__(self):
        self.url_base = 'https://scs.cl.sophia.ac.jp/campusweb/campusportal.do'

        # head-lessモードで起動
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1200x600')

        # .envからユーザ名とパスワードを取得
        dotenv_path = join(dirname(__file__), '.env')
        dotenv.load_dotenv(dotenv_path)
        user_name = os.environ.get('USER_NAME')
        password = os.environ.get('PASSWORD')

        # 起動してログイン
        self.driver = webdriver.Chrome(
            './assets/chromedriver',
            options=options
        )
        self.driver.implicitly_wait(15)
        self.driver.get(self.url_base)
        self.driver.find_element_by_name(
            'userName').send_keys(user_name)
        self.driver.find_element_by_name(
            'password').send_keys(password)
        self.driver.find_element_by_xpath(
            "//input[@value='ログイン']").click()

        # 掲示板にアクセス
        self.driver.find_element_by_id('tab-kj').click()
        # iframe内にドライバを移す
        self.iframe = self.driver.find_element_by_name('portlet-body')
        self.driver.switch_to.frame(self.iframe)

    # 実行日の休講情報の検索
    def search_cancel_announcement(self):
        # '表示期間'のSelectボタンを指定された日に設定
        def set_date_of_select():
            _today = datetime.date.today()
            todays_date_dict = {
                'year': _today.year,
                'month': _today.month,
                'day': _today.day
            }

            html_name_first_list = ['startDay_', 'endDay_']
            html_name_second_list = ['year', 'month', 'day']
            for html_name_first in html_name_first_list:
                for html_name_second in html_name_second_list:
                    html_name = html_name_first + html_name_second
                    element = self.driver.find_element_by_name(html_name)
                    Select(element).select_by_value(
                        str(todays_date_dict[html_name_second])
                    )

        # '表示期間'を指定された日(現状実行した日のみ)にして、
        set_date_of_select()
        time.sleep(3)
        # '履修中のみ'のチェックを外す
        self.driver.find_element_by_name('rishuchuFlg').click()
        # 検索
        self.driver.find_element_by_name('_eventId_search').click()

    # 休講情報のテーブルを作る
    def create_cancel_info_table(self):
        self.search_cancel_announcement()
        cancel_element_list = self.driver.find_elements_by_xpath(
            "//*[@id='entryShowForm']/table[2]/tbody/tr[@class='kyuko-kyuko']/td[5]/a"
        )
        current_handle = self.driver.current_window_handle
        cancel_info_table = []
        for element in cancel_element_list:
            cancel_info_table.append(self.fetch_course_info(element))
            self.driver.switch_to.window(current_handle)
            self.driver.switch_to.frame(self.iframe)

        self.driver.close()
        return cancel_info_table

    # 各講義の休講の詳細を取得
    def fetch_course_info(self, element):
        def fetch_text_data(xpath):
            text = self.driver.find_element_by_xpath(xpath).text
            return correct_str(text)

        def correct_str(_str):
            ret_str = _str.replace('  ', ' ')
            ret_str = re.sub('\u3000', ' ', ret_str)
            ret_str = re.sub('　', ' ', ret_str)
            return ret_str

        element.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

        course_info = {}
        upper_xpath_base = '/html/body/table[1]/tbody/'
        lower_xpath_base = '/html/body/table[2]/tbody/'

        course_info['course_affiliation'] =\
            fetch_text_data(upper_xpath_base + 'tr[1]/td')
        course_info['course_name'] =\
            fetch_text_data(upper_xpath_base + 'tr[2]/td[1]')

        course_info['cancel_reason'] =\
            fetch_text_data(lower_xpath_base + 'tr[2]/td[2]')
        course_info['period'] =\
            fetch_text_data(lower_xpath_base + 'tr[3]/td[2]')
        course_info['instructor'] =\
            fetch_text_data(lower_xpath_base + 'tr[5]/td[2]')

        return course_info


class MakeTweet:
    def __init__(self, cancel_info_table):
        self.cancel_info_table = cancel_info_table

    def create_tweet_list(self):
        tweet_list = [self.get_tweet_text(cancel_info)
                      for cancel_info in self.cancel_info_table]
        return tweet_list

    def get_tweet_text(self, cancel_info):
        period = cancel_info['period']
        course_name = cancel_info['course_name']
        instructor = cancel_info['instructor']
        course_affiliation = cancel_info['course_affiliation']
        cancel_reason = cancel_info['cancel_reason']
        tweet =\
            f'''{period}
科目: {course_name}
教員: {instructor}
開講所属: {course_affiliation}
理由: {cancel_reason}'''

        return tweet


def main():
    scrape_loyola = ScrapeLoyola()
    cancel_info_table = scrape_loyola.create_cancel_info_table()

    make_tweet = MakeTweet(cancel_info_table)
    tweet_list = make_tweet.create_tweet_list()

    manage_twitter = ManageTwitter()
    for tweet in tweet_list:
        manage_twitter.post_tweet(tweet)
    # pprint.pprint(tweet_list)


if __name__ == "__main__":
    main()
