class Generator:
    def __init__(self, destination, check_in_date, check_out_date):
        self.destination = destination
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date

    def generate_file_name(self):
        formatted_destination = self.destination.replace(", ", "_").replace(" ", "_")
        formatted_check_in = self.check_in_date.replace("/", "_")
        formatted_check_out = self.check_out_date.replace("/", "_")
        return (
            f"{formatted_destination}_{formatted_check_in}_To_{formatted_check_out}.csv"
        )
