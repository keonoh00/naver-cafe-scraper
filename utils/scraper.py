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
        self.__search_author(author_name=author_name)

        self.__get_post_lists(author_name=author_name)

    def __get_post_lists(self, author_name):
        """
        작성자의 글 목록을 가져온다.
        """

        print("Getting post lists for: ", author_name)

        posts_containers_with_header = self.browser.find_elements(
            By.CLASS_NAME,
            "article-board",
        )

        for posts_container in posts_containers_with_header:
            if posts_container.get_attribute("id") == "upperArticleList":
                continue

            posts = posts_container.find_elements(By.TAG_NAME, "tr")

            for post in posts:
                author = post.find_element(By.CLASS_NAME, "td_name").text
                # Double check the author name
                if author != author_name:
                    continue

                post_date = post.find_element(
                    By.CLASS_NAME,
                    "td_date",
                ).text

                post_date = post_date.replace(".", "-")[:-1]

                print("Getting post content for: ", post_date)

                clickable = post.find_element(By.CLASS_NAME, "article")
                clickable.click()

                time.sleep(1)

                self.__save_post_content(post_date)

                break

    def __save_post_content(self, post_date):
        pass

    def __search_author(self, author_name):
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

        time.sleep(1)

        # Search Result is given in iframe
        self.browser.switch_to.frame("cafe_main")

        filter_box = self.__debounced_find_element(
            self.browser, By.CLASS_NAME, "search_input"
        )

        dropdown = self.__debounced_find_element(
            filter_box,
            By.ID,
            "divSearchByTop",
        )

        dropdown.click()

        dropdown_ul = self.__debounced_find_element(
            dropdown,
            By.CLASS_NAME,
            "select_list",
        )
        dropdown_li = dropdown_ul.find_elements(By.TAG_NAME, "li")

        for li_fragment in dropdown_li:
            if li_fragment.text == "글작성자":
                li_fragment.click()
                break

        time.sleep(1)

        self.browser.find_element(By.CLASS_NAME, "btn-search-green").click()

        time.sleep(10)

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
