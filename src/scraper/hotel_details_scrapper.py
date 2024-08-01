import time
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))

from utils.logger import logging
from utils.exception import CustomException


class Page:
    def __init__(self, driver, driver_timer):
        self.driver = driver
        self.driver_timer = driver_timer

    def wait_for_element(self, by, value, visibility=False):
        wait_func = (
            EC.visibility_of_element_located
            if visibility
            else EC.presence_of_element_located
        )
        return WebDriverWait(self.driver, timeout=self.driver_timer).until(
            wait_func((by, value))
        )

    def wait_for_elements(self, by, value, visibility=False):
        wait_func = (
            EC.visibility_of_all_elements_located
            if visibility
            else EC.presence_of_all_elements_located
        )
        return WebDriverWait(self.driver, timeout=self.driver_timer).until(
            wait_func((by, value))
        )

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);"
        )
        time.sleep(2)

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)


class HotelPage(Page):
    def get_room_webpage_elements(self, hotel_card):
        hotel_card.click()
        time.sleep(3)
        for i in range(3):
            try:
                hotel_name_element = self.wait_for_element(
                    By.XPATH, '//*[@id="topOfPage"]/div[3]/app-hotel-info-v2/button'
                )
                print(hotel_name_element.text)
                
                room_name_elements = self.wait_for_elements(
                    By.XPATH,
                    '//div[@class="roomInfo"]//h2[contains(@class, "roomName")]',
                    visibility=True,
                )
                price_elements = self.wait_for_elements(
                    By.XPATH,
                    '//div[contains(@class, "total-price")]/span[contains(@class, "cash")]',
                    visibility=True,
                )

                if hotel_name_element and room_name_elements and price_elements:
                    return hotel_name_element, room_name_elements, price_elements
            except TimeoutException:
                logging.error(f"attempt {i+1} for load room webpage elements")
                continue
        return False

    def fetch_room_webpage_data(self, hotel_card):
        if is_element_presence := self.get_room_webpage_elements(hotel_card):
            hotel_name_element, room_name_elements, price_elements = is_element_presence
        else:
            return False

        hotel_name = hotel_name_element.text.strip()
        room_types = [room.text for room in room_name_elements]
        prices = [price.text for price in price_elements]

        return hotel_name, room_types, prices


class HotelScraper:
    def __init__(
        self,
        driver,
        driver_timer,
        destination,
        check_in_date,
        check_out_date,
        available_hotels,
    ):
        self.page = Page(driver, driver_timer)
        self.hotel_page = HotelPage(driver, driver_timer)
        self.destination = destination
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.available_hotels = available_hotels

    def get_hotel_data(self):
        hotel_data = []
        try:
            self.page.scroll_to_top()
        except Exception as e:
            logging.error("failed to scroll to top for hotels page")
            logging.error(f"{CustomException(e,sys)}")

        for index in range(self.available_hotels):
            try:
                if index >= 9:
                    self.page.scroll_to_bottom()
            except Exception as e:
                logging.error("failed to scroll to bottom for hotels page")
                logging.error(f"{CustomException(e,sys)}")

            try:
                hotel_cards = self.page.wait_for_elements(
                    By.XPATH, "//button[contains(text(), 'Select Hotel')]"
                )
            except Exception as e:
                logging.error("failed to load hotel cards")
                logging.error(f"{CustomException(e,sys)}")

            try:
                hotel_card = hotel_cards[index]
            except Exception as e:
                logging.error(
                    f"failed to select hotel cards, total hotel card {len(hotel_cards)}, index {index} , available hotels {self.available_hotels}"
                )
                logging.error(f"{CustomException(e,sys)}")

            if not (
                is_fetch_successful := self.hotel_page.fetch_room_webpage_data(
                    hotel_card
                )
            ):
                logging.error("fetch room webpage data unsuccessful")
                return hotel_data

            hotel_name, room_types, prices = is_fetch_successful
            hotel_data.extend(
                {
                    "Location": self.destination,
                    "Check-in Date": self.check_in_date,
                    "Check-out Date": self.check_out_date,
                    "Hotel Name": hotel_name,
                    "Room Type": room_type,
                    "Price": price,
                }
                for room_type, price in zip(room_types, prices)
            )
            self.page.driver.back()
            time.sleep(3)

            try:
                self.page.scroll_to_bottom()
            except Exception as e:
                logging.error("failed to scroll to bottom for hotels page")
                logging.error(f"{CustomException(e,sys)}")

        return hotel_data
