import pathlib
import csv
import sys
from pathlib import Path
src_path = Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))
from utils.logger import logging
from utils.exception import CustomException

class CSV_storage:

    def __init__(self, destination, hotel_data, file_name):
        self.destination = destination
        self.hotel_data = hotel_data
        self.file_name = file_name

    def modify_float(self, number):
        modified_number = number

        decimal_part = number % 1 
        if decimal_part >= 0.3:
            modified_number += 1 - decimal_part  
        else:
            modified_number -= decimal_part 

        return int(modified_number)

    def save_to_csv(self):
        try:

            # exchange_rate = 0.01198
            # for item in self.hotel_data:
            #     item["Price"] = self.modify_float(
            #         float(item["Price"].replace(",", "")) * exchange_rate
            #     )

            if self.hotel_data:
                keys = self.hotel_data[0].keys()
                base_dir = (
                    pathlib.Path(__file__).parent.parent.parent
                    / "data"
                    / "raw"
                    / self.destination
                )
                base_dir.mkdir(parents=True, exist_ok=True)

                file_path = base_dir / self.file_name

                with file_path.open("w", newline="") as output_file:
                    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(self.hotel_data)
        except Exception as e:
            logging.error("failed to save csv file")
            logging.error(f"{CustomException(e,sys)}")
