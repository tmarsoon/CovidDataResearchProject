class VaccinationData:
    def __init__(self, zip_code, partial_vax, full_vax):
        self.zip_code = zip_code
        self.partial_vax = partial_vax
        self.full_vax = full_vax

    def get_zip_code(self):
        return self.zip_code

    def get_full_vaccinations(self):
        return self.full_vax

    def get_partial_vaccinations(self):
        return self.partial_vax

    def __str__(self):
        return (f"Vaccination data for Zip Code: {self.zip_code}\n"
                f"Partial Vaccinations: {self.partial_vax}\n"
                f"Full Vaccinations: {self.full_vax}\n")