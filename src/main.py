import sys
import time
from datetime import datetime, timedelta
from utils.driver import Driver
from utils.generate import Generator
from utils.logger import logging
from utils.exception import CustomException
from scraper.hotel_count import HotelCount
from scraper.hotel_search import HotelSearchForm
from scraper.hotel_details_scrapper import HotelScraper
from storage.csv_storage import CSV_storage

class Main():
    def __init__(self, DESTINATION, NUMBER_OF_DAYS):
        self.DESTINATION = DESTINATION
        self.NUMBER_OF_DAYS = NUMBER_OF_DAYS
        self.URL = "https://www.ihg.com/hotels/us/en/reservation"
        self.COOKIE_WAIT_TIMER = 5
        self.DRIVER_WAIT_TIMER = 120
        self.DATES = self.create_date_pairs(NUMBER_OF_DAYS)
    
    def create_date_pairs(self, number_of_days):
        num_dates = number_of_days + 1
        start_date = datetime.now()
        dates = [start_date + timedelta(days=i) for i in range(num_dates)]
        date_pairs = list(zip(dates[:-1], dates[1:]))
        return tuple(
            (date1.strftime("%d/%m/%Y"), date2.strftime("%d/%m/%Y"))
            for date1, date2 in date_pairs
        )
            

    def load_driver(self):
        # RETURN THE DRIVER
        driver = Driver(self.URL).get_driver()
        logging.info("succeed to load driver")
        return driver

    def load_hotel_page(self, DRIVER, CHECK_IN_DATE, CHECK_OUT_DATE):
        # LOAD THE HOTELS PAGE
        HotelSearchForm(
            DRIVER,
            self.DRIVER_WAIT_TIMER,
            self.COOKIE_WAIT_TIMER,
            self.DESTINATION,
            CHECK_IN_DATE,
            CHECK_OUT_DATE,
        ).load_hotels_page()

    def calculate_hotels(self, DRIVER):
        # CREATE THE HOTEL COUNT OBJECT
        hotel_count = HotelCount(DRIVER, self.DRIVER_WAIT_TIMER)

        # CALCULATE THE NUMBER OF HOTELS
        total_hotels = hotel_count.get_total_hotels_count()

        # CALCULATE THE NUMBER OF AVAILABLE HOTELS
        self.available_hotels = hotel_count.get_available_hotels_count()

        # RETURN
        # THE NUMBER OF AVAILABLE HOTELS
        return self.available_hotels


    def load_hotel_data(
        self, DRIVER, CHECK_IN_DATE, CHECK_OUT_DATE, available_hotels
    ):
        # RETURN THE SCRAPED HOTEL DATA
        hotel_data = HotelScraper(
            DRIVER,
            self.DRIVER_WAIT_TIMER,
            self.DESTINATION,
            CHECK_IN_DATE,
            CHECK_OUT_DATE,
            available_hotels,
        ).get_hotel_data()
        return hotel_data

    # SCRAPE THE HOTEL DATA & SAVE DATA IN CSV
    def scrape(self):

        # LOOP FOR DATES TO SCRAPE THE HOTEL DATA & SAVE DATA IN CSV
        for CHECK_IN_DATE, CHECK_OUT_DATE in self.DATES:

            # LOAD THE DRIVER
            DRIVER = self.load_driver()

            # LOAD THE HOTELS PAGE
            self.load_hotel_page(DRIVER, CHECK_IN_DATE, CHECK_OUT_DATE)

            # THE NUMBER OF AVAILABLE HOTELS
            available_hotels = self.calculate_hotels(DRIVER)

            # LOAD THE SCRAPED HOTEL DATA
            hotel_data = self.load_hotel_data(
                DRIVER, CHECK_IN_DATE, CHECK_OUT_DATE, available_hotels
            )

            # GENERATE FILE NAME
            file_name = Generator(
                self.DESTINATION, CHECK_IN_DATE, CHECK_OUT_DATE
            ).generate_file_name()

            # SAVE THE HOTEL DATA TO CSV
            CSV_storage(self.DESTINATION, hotel_data, file_name).save_to_csv()

            # QUIT THE DRIVER
            DRIVER.quit()

            # WAIT FOR 3 SECONDS
            time.sleep(3)
