"""
네이버 카페 글 스크래퍼
"""
import os
import time
import math
import pyperclip

from PIL import Image

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver


class NaverCafeScraper:
    def __init__(
        self,
        url,
        user_id,
        password,
        save_dir="./crawl_result",
    ):
        """
        Args:
            url (str): Cafe url
            user_id (str): User ID
            password (str): User Password
            save_dir (str): Directory to save scraped data
        """
        if os.path.exists(save_dir) is False:
            os.mkdir(save_dir)
        self.save_dir = save_dir

        self.chrome_options = Options()
        self.__set_browser_options()

        self.browser: WebDriver = webdriver.Chrome(options=self.chrome_options)
        self.browser.maximize_window()

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
        Getting post lists for author

        Args:
            author_name (str): Author name to scrape

        Returns:
            None
        """
        self.__search_author(author_name=author_name)

        while True:
            # Get and save the post lists from current page
            self.__crawl_current_page()

            next_page_exists = self.__next_page()

            if not next_page_exists:
                try:
                    self.__move_to_next_page_chunks()
                except NotImplementedError:
                    print("No more pages")
                    break

    def __next_page(self) -> bool:
        """
        Go to next page
        """

        # Go to next page
        self.browser.switch_to.frame("cafe_main")
        main_area = self.browser.find_element(By.ID, "main-area")

        WebDriverWait(main_area, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "prev-next")
            )
        )

        prev_next_container = main_area.find_element(
            By.CLASS_NAME,
            "prev-next",
        )
        current_page_idx = int(
            prev_next_container.find_element(
                By.CLASS_NAME,
                "on",
            ).text
        )
        next_page_idx = current_page_idx + 1
        print(f"Going to page {next_page_idx}")

        possible_pages = prev_next_container.find_elements(By.TAG_NAME, "a")

        next_page = None
        for page in possible_pages:
            if page.text == str(next_page_idx):
                next_page = page
                break

        if next_page is None:
            self.browser.switch_to.default_content()
            return False

        next_page.click()

        time.sleep(1)

        self.browser.switch_to.default_content()

        return True

    def __move_to_next_page_chunks(self):
        time.sleep(1)

        self.browser.switch_to.frame("cafe_main")

        main_area = self.browser.find_element(By.ID, "main-area")

        WebDriverWait(main_area, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "prev-next")
            )
        )

        prev_next_container = main_area.find_element(
            By.CLASS_NAME,
            "prev-next",
        )

        next_page_chunk = prev_next_container.find_element(
            By.CLASS_NAME,
            "pgR",
        )

        next_page_chunk.click()

        time.sleep(1)

        self.browser.switch_to.default_content()

    def __crawl_current_page(self):
        """
        Getting post lists for current page
        """

        self.browser.switch_to.frame("cafe_main")

        posts_containers_with_header = self.browser.find_elements(
            By.CLASS_NAME,
            "article-board",
        )

        for posts_container in posts_containers_with_header:
            if posts_container.get_attribute("id") == "upperArticleList":
                continue

            posts_number = len(
                posts_container.find_elements(By.CLASS_NAME, "td_article")
            )
            print(f"Total posts: {posts_number}")

            self.browser.switch_to.default_content()

            for post_idx in range(posts_number):
                print(f"Getting post {post_idx + 1} of {posts_number}")
                self.browser.switch_to.frame("cafe_main")
                posts = self.browser.find_elements(By.CLASS_NAME, "td_article")
                link = posts[post_idx].find_element(By.TAG_NAME, "a")
                link.click()
                time.sleep(3)
                self.__save_post_content()
                self.browser.back()
                time.sleep(3)

    def __save_post_content(self):
        """
        Getting post content
        """

        post_date = (
            self.browser.find_element(
                By.CLASS_NAME,
                "article_info",
            )
            .find_element(
                By.CLASS_NAME,
                "date",
            )
            .text
        )
        post_date = post_date.replace(".", "").replace(" ", "")

        post_title = (
            self.browser.find_element(
                By.CLASS_NAME,
                "title_area",
            )
            .find_element(By.CLASS_NAME, "title_text")
            .text
        )

        # Get out of iframe
        self.browser.switch_to.default_content()

        browser_height = self.browser.execute_script(
            "return window.innerHeight",
        )

        scroll_size = self.browser.execute_script(
            "return document.body.scrollHeight",
        )
        total_sections = math.ceil(scroll_size / browser_height)

        if os.path.exists("temp") is False:
            os.mkdir("temp")

        for section in range(total_sections + 1):
            self.browser.execute_script(
                f"window.scrollTo(0, {section * browser_height})"
            )
            time.sleep(1)

            self.browser.save_screenshot(f"temp/{section}.png")

        images = [
            Image.open(f"temp/{section}.png")
            for section in range(
                total_sections,
            )
        ]

        merged_image = Image.new(
            "RGB",
            (images[0].width, images[0].height * len(images)),
        )

        pasting_position = 0

        for image in images:
            merged_image.paste(image, (0, pasting_position))
            pasting_position += image.height

        merged_image.save(f"{self.save_dir}/{post_date}-{post_title}.png")

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

        time.sleep(3)

        # Get out of iframe
        self.browser.switch_to.default_content()

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
        print("Entering userid: ", self.user_id)
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


methods = [
    "accessible_name",
    "aria_role",
    "clear",
    "click",
    "find_element",
    "find_elements",
    "get_attribute",
    "get_dom_attribute",
    "get_property",
    "id",
    "is_displayed",
    "is_enabled",
    "is_selected",
    "location",
    "location_once_scrolled_into_view",
    "parent",
    "rect",
    "screenshot",
    "screenshot_as_base64",
    "screenshot_as_png",
    "send_keys",
    "shadow_root",
    "size",
    "submit",
    "tag_name",
    "text",
    "value_of_css_property",
]
