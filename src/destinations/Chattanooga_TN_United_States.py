import sys
from pathlib import Path
from datetime import datetime, timedelta


if __name__ == "__main__":
    src_path = Path(__file__).resolve().parent.parent
    sys.path.append(str(src_path))
    
    from main import Main
    from utils.logger import logging
    from utils.exception import CustomException

    destination = "Chattanooga, TN, United States"
    number_of_days = 3
    unique_dates = [(datetime.now() + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(number_of_days)]

    try:
        logging.info(f"scraper is running for {destination} : {unique_dates}")
        Main(destination, number_of_days).scrape()
        logging.info(f"succeed to scrape {destination} : {unique_dates}")
    except Exception as e:
        logging.error(f"failed to scrape {destination} : {unique_dates}")
        logging.error(f"{CustomException(e, sys)}")