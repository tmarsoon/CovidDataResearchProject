import pandas as pd
from datetime import datetime
from edu.upenn.cit594.data.Covid19Data import Covid19Data
from edu.upenn.cit594.datamanagement.FileSuperLogger import FileSuperLogger

class JSONCovidData(FileSuperLogger):

    date_format = "%Y-%m-%d"

    def __init__(self, filename, logger):
        super().__init__(filename, logger)
        self.covid_map = {}

    # org.json.simple.parser.ParseException and java.text.ParseException causes a naming conflict
    # both must be used to throw for the jsonArray parser and the dateFormat variable
    # here we throw the import statement directly to bypass this conflict
    def json_covid_reader(self, json_file):
        try:
            df = pd.read_json(json_file)
            for _, row in df.iterrows():
                # Parsing the JSON data
                zip_code = self.get_int_from_obj(row, "zip_code")
                neg_results = self.get_int_from_obj(row, "NEG")
                pos_results = self.get_int_from_obj(row, "POS")
                tests_conducted = neg_results + pos_results
                deaths = self.get_int_from_obj(row, "deaths")
                hospitalizations = self.get_int_from_obj(row, "hospitalized")
                partial_vax = self.get_int_from_obj(row, "partially_vaccinated")
                full_vax = self.get_int_from_obj(row, "fully_vaccinated")
                boosters = self.get_int_from_obj(row, "boosted")

                # im not seeing a boosted section in the json file
                time_stamp = self.get_date_from_obj(row, "etl_timestamp")
                date = time_stamp.strftime(self.date_format)

                covid_data = Covid19Data(zip_code, time_stamp, partial_vax, full_vax, neg_results,
                                         pos_results, tests_conducted, deaths, hospitalizations, boosters)
                self.covid_map[date] = covid_data

            # Logging the covid event
            self.logger.log_event(self.filename)
        except FileNotFoundError as e:
            # Log file not found error
            self.logger.log_event(f"Error: Covid data isn't found - {self.filename}")
            print(e)
        except IOError as e:
            # Log IO error
            self.logger.log_event(f"Error: Reading covid data file - {self.filename}")
            print(e)
        except ValueError as e:
            # Log parsing errors
            self.logger.log_event(f"Error: Parsing covid data file - {self.filename}")
            print(e)

    """
    helper method to parse file for valid values 
    @param covidData
    @param key
    @return
    """
    def get_int_from_obj(self, covid_data, key):
        # get the object from the map
        object_to_retrieve = covid_data.get(key)

        if pd.notna(object_to_retrieve):
            try:
                # return the parsed int
                return int(object_to_retrieve)
            except ValueError as e:
                # Log parsing errors
                self.logger.log_event(f"Error: Parsing covid data file - {self.filename}")
                print(e)

        # otherwise return 0
        return 0

    """
    helper method to parse file for valid values 
    @param covidData
    @param key
    @return
    @throws java.text.ParseException 
    """
    def get_date_from_obj(self, covid_date_data, key):
        # get the object from the map
        object_to_retrieve = covid_date_data.get(key)

        if pd.notna(object_to_retrieve):
            try:
                # cleaning up the data by removing quotes mark at beginning and end of date field
                covid_date_str = str(object_to_retrieve).strip('"')

                # return the parsed date
                return datetime.strptime(covid_date_str, self.date_format)
            except ValueError as e:
                # Log parsing errors
                self.logger.log_event(f"Error: Parsing covid data file - {self.filename}")
                print(e)

        # otherwise return empty date
        return datetime.now()

    # here we throw the import statement directly to bypass this parseexception naming conflict
    def get_vaccination_number(self, vax_type, date):
        date_format = "%Y-%m-%d"
        # setting a lenient parser to false since when parsing dates, the parser can be lenient
        # setting object to false so the parser strictly follows the format
        date_as_date = datetime.strptime(date, date_format)
        # formatting the date back to a string
        date_str = date_as_date.strftime(date_format)

        # creating covid19data object
        covid_data = self.covid_map.get(date_str)
        # if the date is out of range, there will be no data

        if covid_data is None:
            print(f"No covid data available: {date_str}")
            return 0

        if vax_type.lower() == "full":
            return covid_data.get_fully_vaccinated()
        elif vax_type.lower() == "partial":
            return covid_data.get_partially_vaccinated()
        else:
            print(f"The vaccine does not exist: {vax_type}")
            return 0