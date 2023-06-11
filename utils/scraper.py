"""
네이버 카페 글 스크래퍼
"""
from selenium import webdriver


class NaverCafeScraper:
    """
    1. 로그인
    2. 작성자 검색
    3. 작성자의 글 목록 가져오기
    4. 글 목록에서 글 하나씩 가져오기
    5. 글 내용 가져오기
    """

    def __init__(self, url):
        self.browser = webdriver.Chrome()
        self.url = url

        self.browser.get(url)

        self.__login()

    def scrape_author(
        self,
        author_name,
    ):
        """
        작성자의 글 목록을 가져온다.
        """

    def __login(self):
        pass
