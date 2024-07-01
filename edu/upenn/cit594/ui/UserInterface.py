import sys
from datetime import datetime
from edu.upenn.cit594.logging import Logger
from edu.upenn.cit594.processor import Processor
from decimal import Decimal, ROUND_HALF_UP

class UserInterface:
    def __init__(self, processor: Processor, logger: Logger):
        self.scanner = input  # In Python, we'll use the input() function for reading input
        self.logger = logger
        self.processor = processor

    def read_input(self):
        while True:
            try:
                input_value = int(self.scanner())
                return input_value
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 7. > ")

    def request_user_input(self):
        self.display_menu()
        print("> ", end="")
        sys.stdout.flush()
        return self.read_input()

    def request_5_digit_zip(self):
        while True:
            print("Please enter a 5-digit Zip Code > ", end="")
            sys.stdout.flush()
            try:
                zip_code = int(self.scanner())
                if len(str(zip_code)) == 5:
                    return zip_code
                else:
                    print("Invalid Zip Code. Please enter a 5-digit Zip Code.")
            except ValueError:
                print("Invalid Zip Code. Please enter a 5-digit Zip Code.")

    def display_menu(self):
        print("Which action would you like to perform?")
        print("0. Exit the program.\n"
              "1. Show the available actions.\n"
              "2. Show the total population for all ZIP Codes.\n"
              "3. Show the total vaccinations per capita for each ZIP Code for the specified date.\n"
              "4. Show the average market value for properties in a specified ZIP Code.\n"
              "5. Show the average total livable area for properties in a specified ZIP Code.\n"
              "6. Show the total market value of properties, per capita, for a specified ZIP Code.\n"
              "7. Show the results of your custom feature.")

    def execute_action(self, action, file_type):
        log_message = []
        if action == 0:
            log_message.append("Exiting the program.")
            print("Exiting the program.")
            sys.exit(0)
        elif action == 1:
            self.request_user_input()
        elif action == 2:
            total_population = self.processor.get_total_population()
            log_message.append(f"Total Population: {total_population}")
            print(f"Total Population: {total_population}")
        elif action == 3:
            print("Please enter 'partial' or 'full': ")
            vax_type = self.scanner().lower()
            if vax_type not in ["partial", "full"]:
                print("Invalid vaccination type. Please enter 'partial' or 'full'.")
                return
            print("Please enter the date in the format YYYY-MM-DD: ")
            date = self.scanner()
            if not self.is_valid_date_format(date):
                print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")
                return
            print("BEGIN OUTPUT")
            total_vax_per_capita = self.processor.get_total_vaccinations_per_capita(file_type, vax_type, date)
            print("END OUTPUT")
        elif action == 4:
            specified_zip_code4 = self.request_5_digit_zip()
            log_message.append("Calculating average market value...")
            print("Calculating average market value...")
            average_market_value = self.processor.get_average_market_value(specified_zip_code4)
            formatted_average_market_value = "{:,}".format(average_market_value)
            log_message.append(f"The average Market Value for ZIP Code, {specified_zip_code4}, is ${formatted_average_market_value}")
            print(f"The average Market Value for ZIP Code, {specified_zip_code4}, is ${formatted_average_market_value}")
        elif action == 5:
            specified_zip_code5 = self.request_5_digit_zip()
            log_message.append("Calculating average livable area...")
            print("Calculating average livable area...")
            average_livable_area = self.processor.get_average_livable_area(specified_zip_code5)
            formatted_average_livable_area = "{:,}".format(average_livable_area)
            log_message.append(f"The average Total Livable Area for ZIP Code, {specified_zip_code5}, is {formatted_average_livable_area}")
            print(f"The average Total Livable Area for ZIP Code, {specified_zip_code5}, is {formatted_average_livable_area}")
        elif action == 6:
            specified_zip_code6 = self.request_5_digit_zip()
            log_message.append("Calculating total market value per capita...")
            print("Calculating total market value per capita...")
            total_market_value_per_capita = self.processor.get_total_market_value_per_capita(specified_zip_code6)
            formatted_market_value_per_capita = "{:,}".format(total_market_value_per_capita)
            log_message.append(f"The total Market Value of Properties Per Capita for ZIP Code, {specified_zip_code6}, is ${formatted_market_value_per_capita}")
            print(f"The total Market Value of Properties Per Capita for ZIP Code, {specified_zip_code6}, is ${formatted_market_value_per_capita}")
        elif action == 7:
            specified_zip_code7 = self.request_5_digit_zip()
            print("please wait...")
            log_message.append("please wait...")
            correlation_coefficient = self.processor.calculate_correlation(specified_zip_code7)
            formatted_total_property_value = "{:,}".format(self.processor.get_total_prop_value_per_zip(specified_zip_code7))
            print(f"Total Property Value: ${formatted_total_property_value}")
            log_message.append(f"Total Property Value: ${formatted_total_property_value}")
            formatted_total_population = "{:,}".format(self.processor.get_total_pop_by_zip(specified_zip_code7))
            print(f"Total Population: {formatted_total_population}")
            log_message.append(f"Total Population: {formatted_total_population}")
            print("Calculating correlation coefficient...")
            log_message.append("Calculating correlation coefficient...")
            formatted_average_market_val_per_cap = "{:,}".format(self.processor.get_total_market_value_per_capita(specified_zip_code7))
            print(f"Avaerage Market Value per cap: {formatted_average_market_val_per_cap}")
            log_message.append(f"Avaerage Market Value per cap: {formatted_average_market_val_per_cap}")
            df = Decimal("0.00")
            mean_positivity_rate = self.processor.get_positivity_rate() * Decimal("100.00")
            mean_positivity_rate = mean_positivity_rate.quantize(df, rounding=ROUND_HALF_UP)
            print(f"Mean Positivity Rate: {mean_positivity_rate}%")
            log_message.append(f"Mean Positivity Rate: {mean_positivity_rate}%")
            log_message.append(f"Coefficient Coefficient: {correlation_coefficient}\nInterpretation: ")
            print(f"Coefficient Coefficient: {correlation_coefficient}")
            print("Interpretation: ")
            if correlation_coefficient > 0:
                log_message.append("There is a positive correlation between COVID-19 positivity rates and average market values per capita.")
                print("There is a positive correlation between COVID-19 positivity rates and average market values per capita.")
            elif correlation_coefficient < 0:
                log_message.append("There is a negative correlation between COVID-19 positivity rates and average market values per capita.")
                print("There is a negative correlation between COVID-19 positivity rates and average market values per capita.")
            else:
                log_message.append("There is no significant linear relationship between COVID-19 positivity rates and average market values per capita.")
                print("There is no significant linear relationship between COVID-19 positivity rates and average market values per capita.")
        else:
            log_message.append("Invalid option. Please enter a number between 0 and 7.")
            print("Invalid option. Please enter a number between 0 and 7.")

        self.logger.log_event("\n".join(log_message))

    def is_valid_date_format(self, date):
        """
        Checks if the provided date string has the format YYYY-MM-DD.
        @param date The date string to validate.
        @return true if the date format is valid, false otherwise.
        """
        try:
            # Attempt to parse the date
            date_format = "%Y-%m-%d"
            datetime.strptime(date, date_format)
            return True
        except ValueError:
            return False