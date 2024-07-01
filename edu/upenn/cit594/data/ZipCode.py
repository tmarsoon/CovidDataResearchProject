class ZipCode:
    def __init__(self, zip_code, population):
        self.zip_code = zip_code
        self.population = population
        self.properties = set()
        self.covid19_data = set()

    def add_property(self, property):
        self.properties.add(property)

    def add_covid19_data(self, covid19_data):
        self.covid19_data.add(covid19_data)

    def get_zip_code(self):
        return self.zip_code

    def set_zip_code(self, zip_code):
        self.zip_code = zip_code

    def get_population(self):
        return self.population

    def set_population(self, population):
        self.population = population

    def get_properties(self):
        return self.properties

    def set_properties(self, properties):
        self.properties = properties

    def get_covid19_data(self):
        return self.covid19_data

    def set_covid19_data(self, covid19_data):
        self.covid19_data = covid19_data