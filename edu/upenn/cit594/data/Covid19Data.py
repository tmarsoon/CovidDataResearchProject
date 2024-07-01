from datetime import datetime

class Covid19Data:
    """
      Represents Covid-19 data for a specific area and time.

      Attributes:
          zip_code (int): Represents where the vaccinations were provided.
          time_stamp (datetime): Utilizes the Date data type to represent YYYY-MM-DD hh:mm:ss.
          partially_vaccinated (int): The total number of people who have their first vaccine dose, but not their second.
          fully_vaccinated (int): Total number of people who have received their second vaccine dose.
          negative_result (int): Total number of covid tests that had a negative result.
          positive_result (int): Total number of covid tests that had a positive result.
          tests_conducted (int): Total number of covid infection tests given.
          deaths (int): Total number of people that have died from covid.
          covid_hospitalizations (int): Total number of all people (living or deceased) that have been administered to the hospital.
          boosters_given (int): Total number of boosters given.
      """
    def __init__(self, zip_code, time_stamp, partially_vaccinated, fully_vaccinated,
                 negative_result, positive_result, tests_conducted, deaths, covid_hospitalizations, boosters_given):
        self.zip_code = zip_code
        self.time_stamp = time_stamp
        self.partially_vaccinated = partially_vaccinated
        self.fully_vaccinated = fully_vaccinated
        # The remaining variables are for the free-form analysis in part 3.7
        self.negative_result = negative_result
        self.positive_result = positive_result
        self.tests_conducted = tests_conducted
        self.deaths = deaths
        self.covid_hospitalizations = covid_hospitalizations
        self.boosters_given = boosters_given

    def get_zip_code(self):
        return self.zip_code

    def get_time_stamp(self):
        return self.time_stamp

    def get_partially_vaccinated(self):
        return self.partially_vaccinated

    def get_fully_vaccinated(self):
        return self.fully_vaccinated

    def get_negative_result(self):
        return self.negative_result

    def get_tests_conducted(self):
        # Total number of covid infection tests given
        self.tests_conducted = self.negative_result + self.positive_result
        return self.tests_conducted

    def get_deaths(self):
        return self.deaths

    def get_covid_hospitalizations(self):
        return self.covid_hospitalizations

    def get_boosters_given(self):
        return self.boosters_given

    def get_pos_results(self):
        return self.positive_result

    def get_neg_results(self):
        return self.negative_result