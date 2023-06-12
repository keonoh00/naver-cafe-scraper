"""
네이버 카페 글 스크래퍼
"""
import os
import time
import pyperclip


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class NaverCafeScraper:
    """
    1. 로그인
    2. 작성자 검색
    3. 작성자의 글 목록 가져오기
    4. 글 목록에서 글 하나씩 가져오기
    5. 글 내용 가져오기
    """

    def __init__(
        self,
        url,
        user_id,
        password,
    ):
        self.chrome_options = Options()
        self.__set_browser_options()

        self.browser = webdriver.Chrome(options=self.chrome_options)

        self.url = url
        self.user_id = user_id
        self.password = password

        self.browser.get(url)

        time.sleep(1)

        self.__login()

    def scrape_author(
        self,
        author_name,
    ):
        """
        작성자의 글 목록을 가져온다.
        """

        search_box = self.__debounced_find_element(
            self.browser,
            By.ID,
            "cafe-search",
            30,
        )

        search_input = search_box.find_element(By.ID, "topLayerQueryInput")
        search_input.click()
        self.__paste_to_browser(search_input, author_name)
        print("Searching for author: ", author_name)

        search_box.find_element(By.CLASS_NAME, "btn").click()

    def __set_browser_options(self):
        # self.chrome_options.add_experimental_option(
        #     "detach", True
        # )  # Keep browser open after script ends
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"]
        )  # Remove selenium logging

    def __login(self):
        self.browser.find_element(By.CLASS_NAME, "gnb_btn_login").click()

        # Entering user id
        id_row = self.__debounced_find_element(
            self.browser,
            By.ID,
            "id_line",
        )
        id_input = self.__debounced_find_element(
            id_row,
            By.CLASS_NAME,
            "input_text",
        )
        id_input.click()
        print("Entering user id: ", self.user_id)
        self.__paste_to_browser(id_input, self.user_id)

        # Entering password
        pw_row = self.__debounced_find_element(
            self.browser,
            By.ID,
            "pw_line",
        )
        pw_input = self.__debounced_find_element(
            pw_row,
            By.CLASS_NAME,
            "input_text",
        )
        pw_input.click()
        self.__paste_to_browser(pw_input, self.password)

        time.sleep(1.2)

        self.browser.find_element(By.CLASS_NAME, "btn_login").click()

        time.sleep(3)

    def __debounced_find_element(
        self,
        element,
        by: By,
        value: str,
        time_out: int = 10,
    ):
        try:
            time.sleep(1)
            found_element = WebDriverWait(element, time_out).until(
                expected_conditions.presence_of_element_located((by, value))
            )
            time.sleep(1)

            return found_element

        except NoSuchElementException:
            return element

    def __paste_to_browser(self, element, text):
        pyperclip.copy(text)
        if os.name == "nt":
            element.send_keys(Keys.CONTROL, "v")
        else:
            element.send_keys(Keys.COMMAND, "v")
