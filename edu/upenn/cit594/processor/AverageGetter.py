
class AverageInterface:
    def get_average(self, total_value, properties_number):
        raise NotImplementedError("Subclasses should implement this!")


class AverageGetter(AverageInterface):
    """
    This class implements the interface and provides a case-by-case strategy to calculate averages
    """
    def get_average(self, total_value, properties_number):
        return int(total_value / properties_number)