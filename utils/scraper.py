"""
네이버 카페 글 스크래퍼
"""
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


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
        self.browser = webdriver.Chrome()
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
        )
        search_box.find_element(By.ID, "topLayerQueryInput").send_keys(
            author_name,
        )
        search_box.find_element(By.CLASS_NAME, "btn").click()

    def __login(self):
        self.browser.find_element(By.CLASS_NAME, "gnb_btn_login").click()

        id_row = self.__debounced_find_element(
            self.browser,
            By.ID,
            "id_line",
        )

        pw_row = self.__debounced_find_element(
            self.browser,
            By.ID,
            "pw_line",
        )

        id_input = self.__debounced_find_element(
            id_row,
            By.CLASS_NAME,
            "input_text",
        )
        id_input.send_keys(self.user_id)

        pw_input = self.__debounced_find_element(
            pw_row,
            By.CLASS_NAME,
            "input_text",
        )

        pw_input.send_keys(self.password)

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
            time.sleep(3)
            found_element = WebDriverWait(element, time_out).until(
                expected_conditions.presence_of_element_located((by, value))
            )
            time.sleep(1)

            return found_element

        except FileNotFoundError:
            return element
