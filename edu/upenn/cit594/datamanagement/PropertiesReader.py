import pandas as pd
from edu.upenn.cit594.data.Property import Property
from edu.upenn.cit594.datamanagement.FileSuperLogger import FileSuperLogger
from edu.upenn.cit594.logging.Logger import Logger

class PropertiesReader(FileSuperLogger):
    def __init__(self, filename, logger: Logger):
        super().__init__(filename, logger)
        self.market_value_column = -1
        self.total_livable_area_column = -1
        self.zip_code_column = -1

    def read_properties(self, property_map):
        try:
            df = pd.read_csv(self.filename)
            market_values = df['market_value'].apply(self.parse_property, default_value=0.0).values
            livable_areas = df['total_livable_area'].apply(self.parse_property, default_value=0.0).values
            zip_codes = df['zip_code'].apply(self.parse_integer).values

            for market_value, livable_area, zip_code in zip(market_values, livable_areas, zip_codes):
                if zip_code in property_map:
                    property_map[zip_code].add_property(Property(market_value, livable_area, zip_code))
            self._logger.log_event(f"Read properties data from {self.filename}")
        except FileNotFoundError as e:
            self._logger.log_event(f"File not found: {self.filename}")
        except Exception as e:
            self._logger.log_event(f"Error reading properties data: {str(e)}")

    def parse_property(self, value, default_value):
        try:
            return float(value)
        except ValueError:
            return default_value

    def parse_integer(self, data_to_parse):
        if pd.notna(data_to_parse) and data_to_parse != '':
            try:
                return int(data_to_parse)
            except ValueError as e:
                self._logger.log_event(f"Error parsing integer from property data file - {self.filename}: {e}")
                print(e)
        return -1

    def locate_column(self, columns):
        for i, column in enumerate(columns):
            if column == "market_value":
                self.market_value_column = i
            elif column == "total_livable_area":
                self.total_livable_area_column = i
            elif column == "zip_code":
                self.zip_code_column = i