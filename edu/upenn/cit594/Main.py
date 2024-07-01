import os
import sys
from edu.upenn.cit594.datamanagement.CSVCovidData import CSVCovidData
from edu.upenn.cit594.datamanagement.JSONCovidData import JSONCovidData
from edu.upenn.cit594.datamanagement.PopulationReader import PopulationReader
from edu.upenn.cit594.datamanagement.PropertiesReader import PropertiesReader
from edu.upenn.cit594.logging.Logger import Logger
from edu.upenn.cit594.processor.Processor import Processor
from edu.upenn.cit594.ui.UserInterface import UserInterface

def is_valid_covid19_format(format):
    return format.endswith("csv") or format.endswith("json")

def main(args):
    if len(args) != 4:
        print("Error in runtime arguments.")
        return

    file_type = ""
    covid_data_file = args[0]
    properties_data_file = args[1]
    population_data_file = args[2]
    log_file = args[3]

    if not (os.path.exists(covid_data_file) and os.path.exists(properties_data_file) and os.path.exists(population_data_file)):
        print("One or more input files do not exist.")
        return

    try:
        with open(log_file, 'a'):
            pass
    except Exception as e:
        print(f"Error has occurred during the process of creating/opening the log file: {e}")
        return

    if not is_valid_covid19_format(covid_data_file):
        print("Error: File format not supported in this program.")
        return

    logger = Logger.get_instance()
    logger.change_output_dest(log_file)
    logger.log_event(log_file)
    logger.log_command_line_args(args)

    properties_reader = PropertiesReader(properties_data_file, logger)
    population_reader = PopulationReader(population_data_file, logger)
    csv_covid_reader = CSVCovidData(covid_data_file, logger)
    json_covid_reader = JSONCovidData(covid_data_file, logger)

    if covid_data_file.endswith(".csv"):
        print("Reading COVID CSV data...")  # Debug print statement
        csv_covid_reader.csv_covid_reader()
        file_type = "csv"
    else:
        json_covid_reader.json_covid_reader()
        file_type = "json"

    print("Please wait while we process the data...")
    processor = Processor(csv_covid_reader, json_covid_reader, population_reader, properties_reader, logger)

    ui = UserInterface(processor, logger)
    user_action = ui.request_user_input()
    ui.execute_action(user_action, file_type)

if __name__ == "__main__":
    main(sys.argv[1:])