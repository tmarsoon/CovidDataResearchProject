import pandas as pd
import numpy as np
from edu.upenn.cit594.data.Covid19Data import Covid19Data
from edu.upenn.cit594.datamanagement.FileSuperLogger import FileSuperLogger
from edu.upenn.cit594.logging.Logger import Logger
from datetime import datetime


class CSVCovidData(FileSuperLogger):
    date_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, filename, logger: Logger):
        super().__init__(filename, logger)
        self.covid_map = {}

    def get_covid_map(self):
        """
        Returns the covid map.

        Returns:
            dict: A dictionary containing covid data.
        """
        return self.covid_map

    def csv_covid_reader(self):
        try:
            df = pd.read_csv(self.filename, header=None, dtype=str)
            df.fillna('', inplace=True)

            zip_codes = np.array([self.parse_integer(val) for val in df.iloc[:, 0]])
            neg_results = np.array([self.parse_integer(val) for val in df.iloc[:, 1]])
            pos_results = np.array([self.parse_integer(val) for val in df.iloc[:, 2]])
            deaths = np.array([self.parse_integer(val) for val in df.iloc[:, 3]])
            hospitalizations = np.array([self.parse_integer(val) for val in df.iloc[:, 4]])
            partial_vax = np.array([self.parse_integer(val) for val in df.iloc[:, 5]])
            full_vax = np.array([self.parse_integer(val) for val in df.iloc[:, 6]])
            boosters = np.array([self.parse_integer(val) for val in df.iloc[:, 7]])
            time_stamps = np.array([self.parse_date(val) for val in df.iloc[:, 8]])

            for zip_code, neg, pos, death, hosp, partial, full, boost, time_stamp in zip(zip_codes, neg_results, pos_results, deaths, hospitalizations, partial_vax, full_vax, boosters, time_stamps):
                if zip_code == -1 or time_stamp is None:
                    continue
                covid_data = Covid19Data(zip_code, time_stamp, partial, full, neg, pos, neg + pos, death, hosp, boost)
                if zip_code not in self.covid_map:
                    self.covid_map[zip_code] = []
                self.covid_map[zip_code].append(covid_data)
            self._logger.log_event(f"Read COVID data from {self.filename}")
        except FileNotFoundError as e:
            self._logger.log_event(f"File not found: {self.filename}")
        except Exception as e:
            self._logger.log_event(f"Error reading COVID data: {str(e)}")

    def parse_integer(self, data_to_parse):
        """
        Helper method to parse integers and avoid null or empty strings.

        Args:
            data_to_parse (str): The data to parse.

        Returns:
            int: The parsed integer or -1 if parsing fails.
        """
        if pd.notna(data_to_parse) and data_to_parse != '':
            try:
                return int(data_to_parse)
            except ValueError as e:
                self._logger.log_event(f"Error parsing integer from covid data file - {self.filename}: {e}")
        return -1

    def parse_date(self, data_to_parse):
        """
        Helper method to parse Dates and avoid null or empty strings.

        Args:
            data_to_parse (str): The data to parse.

        Returns:
            datetime: The parsed date or None if parsing fails.
        """
        if pd.notna(data_to_parse) and data_to_parse != '':
            try:
                data_to_parse = data_to_parse.strip('"')
                return datetime.strptime(data_to_parse, self.date_format)
            except ValueError as e:
                self._logger.log_event(f"Error parsing date from covid data file - {self.filename}: {e}")
        return None

    def get_vaccination_number(self, vax_type, date):
        try:
            date_as_date = datetime.strptime(date, "%Y-%m-%d")
            date_str = date_as_date.strftime("%Y-%m-%d")

            vaccination_count = 0
            for zip_code, covid_data_list in self.covid_map.items():
                for covid_data in covid_data_list:
                    if covid_data.time_stamp.strftime("%Y-%m-%d") == date_str:
                        if vax_type.lower() == "full":
                            vaccination_count += covid_data.full_vaccinations
                        elif vax_type.lower() == "partial":
                            vaccination_count += covid_data.partial_vaccinations
            return vaccination_count

        except ValueError as e:
            print(f"Invalid date format provided: {date}")
            return 0