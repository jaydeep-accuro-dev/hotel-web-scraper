import time
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
src_path = Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))
from utils.logger import logging
from utils.exception import CustomException


class HotelCount:
    def __init__(self, driver, driver_timer):
        self.driver = driver
        self.driver_timer = driver_timer

    def get_total_hotels_count(self):
        try:
            hotel_count_element = WebDriverWait(
                driver=self.driver, timeout=self.driver_timer
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//div[contains(@class, "rooms-count-container")]/div[contains(@class, "rooms-count")]/div',
                    )
                )
            )
            hotel_count = int(hotel_count_element.text.split()[0])
            logging.info(f"succeed to calculate total hotels {hotel_count}")
            return hotel_count
        except Exception as e:
            logging.error("failed to calculate total hotels")
            logging.error(f"{CustomException(e,sys)}")
            
    def get_available_hotels_count(self):
        try:
            hotel_count = 0

            for _ in range(3):
                scroll_amount = (
                    self.driver.execute_script(
                        "return document.documentElement.scrollHeight"
                    )
                    / 2
                )
                self.driver.execute_script(f"window.scrollTo(0, {scroll_amount});")

                time.sleep(3)

                hotel_elements = WebDriverWait(self.driver, self.driver_timer).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//button[contains(text(), 'Select Hotel')]")
                    )
                )

                hotel_count = max(hotel_count, len(hotel_elements))

            logging.info(f"succeed to calculate available hotels {hotel_count}")
            return hotel_count
        except Exception as e:
            logging.error("failed to calculate available hotels")
            logging.error(f"{CustomException(e,sys)}")
            