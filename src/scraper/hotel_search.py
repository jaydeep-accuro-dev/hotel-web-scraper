import time
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))

from utils.logger import logging
from utils.exception import CustomException


class HotelSearchForm:
    def __init__(
        self,
        driver,
        driver_timer,
        cookie_timer,
        destination,
        check_in_date,
        check_out_date,
    ):
        self.driver = driver
        self.driver_timer = driver_timer
        self.cookie_timer = cookie_timer
        self.destination = destination
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date

    def _enter_destination(self):
        dest_input = WebDriverWait(driver=self.driver, timeout=self.driver_timer).until(
            EC.element_to_be_clickable((By.ID, "dest-input"))
        )
        dest_input.send_keys(self.destination)
        dest_input.send_keys(Keys.RETURN)

    def _enter_dates(self):
        check_in_date_input = WebDriverWait(
            driver=self.driver, timeout=self.driver_timer
        ).until(EC.element_to_be_clickable((By.ID, "checkInDate")))
        check_in_date_input.click()
        check_in_date_input.send_keys(self.check_in_date)
        check_in_date_input.send_keys(Keys.RETURN)

        check_out_date_input = WebDriverWait(
            driver=self.driver, timeout=self.driver_timer
        ).until(EC.element_to_be_clickable((By.ID, "checkInDate")))
        check_out_date_input.click()
        check_out_date_input.send_keys(self.check_out_date)
        check_out_date_input.send_keys(Keys.RETURN)

    def _search_hotels(self):
        search_button = WebDriverWait(
            driver=self.driver, timeout=self.driver_timer
        ).until(EC.element_to_be_clickable((By.CLASS_NAME, "search-button")))
        search_button.click()

    def _accept_cookies(self):
        accept_button = WebDriverWait(
            driver=self.driver, timeout=self.driver_timer
        ).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@id='truste-consent-button' and contains(text(), 'Continue')]",
                )
            )
        )
        accept_button.click()

    def load_hotels_page(self):

        try:
            self._enter_destination()
            logging.info("succeed to enter destination")
        except Exception as e:
            logging.error("failed to enter destination")
            logging.error(f"{CustomException(e,sys)}")

        try:
            self._enter_dates()
            logging.info("succeed to enter dates")
        except Exception as e:
            logging.error("failed to enter dates")
            logging.error(f"{CustomException(e,sys)}")

        try:
            self._search_hotels()
            logging.info("succeed to search hotels")
        except Exception as e:
            logging.error("failed to search hotels")
            logging.error(f"{CustomException(e,sys)}")

        # time.sleep(self.cookie_timer)
        # logging.info(f"wait for {self.cookie_timer} seconds to load cookie button")

        # try:
        #     self._accept_cookies()
        #     logging.info("succeed to click on cookie button")
        # except Exception as e:
        #     logging.error("failed to click on cookie button")
        #     logging.error(f"{CustomException(e,sys)}")
