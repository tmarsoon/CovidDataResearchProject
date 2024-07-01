class Property:
    def __init__(self, market_value, total_livable_area, zip_code, code):
        self.market_value = market_value
        self.total_livable_area = total_livable_area
        self.zip_code = zip_code
        self.code = code

    def get_market_value(self):
        return self.market_value

    def set_market_value(self, market_value):
        self.market_value = market_value

    def get_total_livable_area(self):
        return self.total_livable_area

    def set_total_livable_area(self, total_livable_area):
        self.total_livable_area = total_livable_area

    def get_zip_code(self):
        return self.zip_code

    def set_zip_code(self, zip_code):
        self.zip_code = zip_code