class AvailableActions:
    """
    diplays the menu of options to the user based on the file used
    @param args
    """

    def display_menu(self, args):
        print("BEGIN OUTPUT")
        available_options = self.display_available_options(args)
        # print each option to console
        for option in available_options:
            print(option)
        print("END OUTPUT")

    def display_available_options(self, args):
        available_options = []
        # 0 and 1 are always valid options
        available_options.append(0)
        available_options.append(1)

        # adding options based on file
        if self.has_covid_file(args):
            available_options.append(3)

        if self.has_properties_file(args):
            available_options.append(4)
            available_options.append(5)
            available_options.append(6)

        if self.has_population_file(args):
            available_options.append(2)

        # returning the list of option
        return available_options

    def has_population_file(self, args):
        for arg in args:
            # split at the = sign
            parts = arg.split("=")
            if len(parts) == 2:
                name = parts[0]
                if name == "--population":
                    return True
        return False

    def has_properties_file(self, args):
        for arg in args:
            # split at the = sign
            parts = arg.split("=")
            if len(parts) == 2:
                name = parts[0]
                if name == "--properties":
                    return True
        return False

    def has_covid_file(self, args):
        for arg in args:
            # split at the = sign
            parts = arg.split("=")
            if len(parts) == 2:
                name = parts[0]
                if name == "--covid":
                    return True
        return False