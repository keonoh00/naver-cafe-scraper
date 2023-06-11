from selenium import webdriver


if __name__ == "__main__":
    browser = webdriver.Chrome()

    browser.get("https://www.google.com")
    browser.quit()
