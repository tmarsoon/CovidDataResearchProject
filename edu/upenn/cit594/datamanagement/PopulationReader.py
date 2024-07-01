import pandas as pd
from edu.upenn.cit594.data.ZipCode import ZipCode
from edu.upenn.cit594.datamanagement.FileSuperLogger import FileSuperLogger
from edu.upenn.cit594.logging.Logger import Logger

class PopulationReader(FileSuperLogger):
    def __init__(self, population_data_file, logger: Logger):
        super().__init__(population_data_file, logger)
        self.population_map = {}

    def read_population_data(self):
        try:
            df = pd.read_csv(self.filename, header=None)
            zip_codes = df.iloc[:, 0].apply(self.parse_integer).values
            populations = df.iloc[:, 1].apply(self.parse_integer).values

            for zip_code, population in zip(zip_codes, populations):
                if zip_code != -1 and population != -1:
                    self.population_map[zip_code] = ZipCode(zip_code, population)
            self._logger.log_event(f"Read population data from {self.filename}")
        except FileNotFoundError as e:
            self._logger.log_event(f"File not found: {self.filename}")
        except Exception as e:
            self._logger.log_event(f"Error reading population data: {str(e)}")

    def parse_integer(self, data_to_parse):
        if pd.notna(data_to_parse) and data_to_parse != '':
            try:
                return int(data_to_parse)
            except ValueError as e:
                self._logger.log_event(f"Error parsing integer from population data file - {self.filename}: {e}")
                print(e)
        return -1

    def get_population_map(self):
        return self.population_map