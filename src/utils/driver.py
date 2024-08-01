import time
import sys
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from pathlib import Path
src_path = Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))
from utils.logger import logging
from utils.exception import CustomException
# from webdriver_manager.chrome import ChromeDriverManager

class Driver:

    def __init__(self, url):
        self.url = url

    def _get_options(self):
        options = ChromeOptions()

        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extentsions")
        options.add_argument("--disable-infobars")
        options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        return options

    def get_driver(self):
        try:
            options = self._get_options()
            
            # For Linux
            chrome_driver = Chrome(
                options=options,
                # service=Service("/usr/local/bin/chromedriver"),
            )
            chrome_driver.get(self.url)
            chrome_driver.maximize_window()
            time.sleep(3)
            return chrome_driver
        except Exception as e:
            print(f"{CustomException(e,sys)}")
            logging.error("failed to load driver")
            logging.error(f"{CustomException(e,sys)}")