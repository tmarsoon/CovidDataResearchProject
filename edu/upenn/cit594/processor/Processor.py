import pandas as pd
import numpy as np
from edu.upenn.cit594.datamanagement import CSVCovidData, JSONCovidData, PopulationReader, PropertiesReader
from edu.upenn.cit594.logging.Logger import Logger
from edu.upenn.cit594.processor import AverageGetter


class Processor:
    def __init__(self, ccd: CSVCovidData, jcd: JSONCovidData, popr: PopulationReader, propr: PropertiesReader, logger: Logger):
        self.csv_covid_reader = ccd
        self.json_covid_reader = jcd
        self.population_reader = popr
        self.properties_reader = propr
        self.logger = logger
        self.population_map = {}

        try:
            self.data_start()
        except FileNotFoundError as e:
            self.logger.log_event(str(e))
        except IOError as e:
            self.logger.log_event(str(e))

    def get_population_map(self):
        return self.population_map

    def data_start(self):
        try:
            print("Reading population data...")
            self.population_reader.read_population_data()
            self.population_map = self.population_reader.get_population_map()
            print("Population Map in Processor:", self.population_map)
        except (FileNotFoundError, pd.errors.ParserError, ValueError) as e:
            self.logger.log_event(str(e))
        print("Reading property data...")
        self.properties_reader.read_properties(self.population_map)

    mem_pop = 0

    def get_total_population(self):
        print("Calculating total population...")
        if self.mem_pop == 0:
            total_population = 0
            for zip_code in self.population_map.values():
                print(f"Processing ZIP Code: {zip_code.get_zip_code()} with population {zip_code.get_population()}")
                total_population += zip_code.get_population()
            self.logger.log_event(f"Total population calculated: {total_population}")
            self.mem_pop = total_population
        return self.mem_pop

    def get_average_market_value(self, zip_code):
        try:
            self.data_start()
        except FileNotFoundError as e:
            self.logger.log_event(str(e))
        except IOError as e:
            self.logger.log_event(str(e))
        if zip_code in self.mem_value:
            return self.mem_value[zip_code]
        else:
            property_count = 0
            sum_market_value = 0
            average_market_value = 0
            if zip_code in self.population_map:
                code = self.population_map[zip_code]
                for property in code.get_properties():
                    sum_market_value += property.get_market_value()
                    property_count += 1
                    print(f"{property_count}: {property.get_market_value()}")
                average = AverageGetter()
                average_market_value = average.get_average(sum_market_value, len(code.get_properties()))
            else:
                print("No data available or invalid ZipCode")
            self.mem_value[zip_code] = average_market_value
            return average_market_value

    def get_average_livable_area(self, zip_code):
        try:
            self.data_start()
        except FileNotFoundError as e:
            self.logger.log_event(str(e))
        except IOError as e:
            self.logger.log_event(str(e))
        if zip_code in self.mem_area:
            return self.mem_area[zip_code]
        else:
            sum_livable_area = 0
            average_livable_area = 0
            if zip_code in self.population_map:
                code = self.population_map[zip_code]
                number_of_properties = len(code.get_properties())
                if number_of_properties == 0:
                    print("No properties available for the specified ZIP Code.")
                    return 0
                for property in code.get_properties():
                    sum_livable_area += property.get_total_livable_area()
                average_getter = AverageGetter()
                average_livable_area = average_getter.get_average(sum_livable_area, number_of_properties)
            else:
                print("Invalid or unavailable ZIP Code.")
                return 0
            self.mem_area[zip_code] = average_livable_area
            return average_livable_area
#the below is a customized designed we added to our project
    def calculate_correlation(self, zip_code4):
        total_property_value = self.get_total_prop_value_per_zip(zip_code4)
        total_population = self.get_total_pop_by_zip(zip_code4)
        mean_property_value = np.mean(total_property_value)
        mean_population = np.mean(total_population)
        covariance = np.cov(self.calculate_positivity_rates().values(), total_property_value)
        std_dev_positivity_rate = np.std(self.calculate_positivity_rates().values())
        std_dev_property_value = np.std(total_property_value)
        correlation_coefficient = covariance / (std_dev_positivity_rate * std_dev_property_value * mean_population)
        return correlation_coefficient

    def calculate_mean(self, data):
        return np.mean(list(data.values()))

    def calculate_standard_deviation(self, data, mean):
        return np.std(list(data.values()))

    def calculate_standard_deviation2(self, total_property_value, mean):
        return np.std(total_property_value)

    def calculate_positivity_rates(self):
        positivity_rates = {}
        for date in self.csv_covid_reader.get_covid_map().keys():
            covid_data = self.csv_covid_reader.get_covid_map().get(date)
            positive_cases = covid_data.get_pos_results()
            total_tests = covid_data.get_neg_results() + positive_cases
            positivity_rate = positive_cases / total_tests
            positivity_rates[date] = positivity_rate
        return positivity_rates