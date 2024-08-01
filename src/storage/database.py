import mysql.connector
import datetime
import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))

from utils.logger import logging
from utils.exception import CustomException


class HotelDataStorage:
    """
    A class to store hotel data in a MySQL database.
    """

    def __init__(self, destination, hotel_data):
        """
        Initializes the class with destination, hotel data, and database configuration.

        Args:
            destination (str): The destination for the hotel data.
            hotel_data (list): A list of dictionaries containing hotel information.
            database_config (dict): A dictionary containing database connection details.
        """

        database_config = {
            "host": "localhost",
            "user": "jaydeep",
            "password": "jaydeep@2002",
            "database": "hotel",
        }

        self.destination = destination
        self.hotel_data = hotel_data
        self.database_config = database_config

    def modify_float(self, number):
        modified_number = number

        decimal_part = number % 1  # Extract decimal part
        if decimal_part >= 0.3:
            modified_number += 1 - decimal_part  # Round up if >= 0.3
        else:
            modified_number -= decimal_part  # Round down otherwise

        return int(modified_number)

    def save_to_mysql(self):
        """
        Converts hotel data prices to USD, creates a table if it doesn't exist,
        and inserts the data into the MySQL database, handling date format conversion.

        Raises:
            mysql.connector.Error: If there's an error connecting to the database or executing queries.
        """
        exchange_rate = 0.01198

        # Convert prices to dollars and update data
        for item in self.hotel_data:
            item["Price"] = self.modify_float(
                float(item["Price"].replace(",", "")) * exchange_rate
            )

        # Connect to MySQL database
        connection = None
        try:
            connection = mysql.connector.connect(**self.database_config)
            cursor = connection.cursor()

            # Create table if it doesn't exist
            create_table_query = """
                CREATE TABLE IF NOT EXISTS hotels (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    location VARCHAR(255) NOT NULL,
                    check_in_date DATE NOT NULL,
                    check_out_date DATE NOT NULL,
                    hotel_name VARCHAR(255) NOT NULL,
                    room_type VARCHAR(255) NOT NULL,
                    price INT NOT NULL
                )
            """
            cursor.execute(create_table_query)
            connection.commit()

            # Insert data into the table with date format conversion (YYYY-MM-DD)
            insert_query = """
                INSERT INTO hotels (location, check_in_date, check_out_date, hotel_name, room_type, price)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            # Use a list comprehension to prepare data tuples with formatted dates
            data_tuples = [
                (
                    item["Location"],
                    datetime.datetime.strptime(
                        item["Check-in Date"], "%d/%m/%Y"
                    ).strftime("%Y-%m-%d"),
                    datetime.datetime.strptime(
                        item["Check-out Date"], "%d/%m/%Y"
                    ).strftime("%Y-%m-%d"),
                    item["Hotel Name"],
                    item["Room Type"],
                    str(item["Price"]),
                )
                for item in self.hotel_data
            ]

            cursor.executemany(insert_query, data_tuples)
            connection.commit()
        except mysql.connector.Error as err:
            logging.error("Error saving data to MySQL")
            logging.error(f"{CustomException(err, sys)}")
        finally:
            if connection:
                cursor.close()
                connection.close()
