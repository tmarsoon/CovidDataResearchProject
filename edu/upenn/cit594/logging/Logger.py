import sys
import time


class Logger:
    instance = None

    def __init__(self):
        # Initializing the logger to have a standard error output since the main method may be invoked multiple times
        self.output = sys.stderr

    @staticmethod
    def get_instance():
        if Logger.instance is None:
            Logger.instance = Logger()
        return Logger.instance

    """
    Logging an event with a timestamp
    The timestamp here will be printed before the message is sent to the logger
    @param event  The event message
    """

    def log_event(self, event):
        timestamp = int(time.time() * 1000)
        print(f"{timestamp} {event}", file=self.output)

    """
    sets the output file destination.
    If the previous destination is a file, it will be closed while switching.
    @param file_to_write  File that the Logger writes to
    """

    def change_output_dest(self, file_to_write):
        # if a file exists, output should be closed
        if self.output != sys.stderr:
            self.output.close()

        # if the file is empty or contains no content, output the error and return void
        if not file_to_write:
            self.output = sys.stderr
            return

        # if necessary, attempt to append the log file
        try:
            # append to the specified log file
            self.output = open(file_to_write, 'a')
        except FileNotFoundError:
            # If unable to create the log file, revert to standard error
            print(f"Unable to open log file: {file_to_write}", file=sys.stderr)
            self.output = sys.stderr

    """
    logs the command line arguments
    @param args
    """

    def log_command_line_args(self, args):
        # creating a string builder object since SB can be modified
        # append() will automatically initiate a capacity update to the object
        string_build = "Command Line Arguments: " + " ".join(args) + " "
        self.log_event(string_build)

    """
    logs the name of the input file
    @param input_file
    """

    def log_input_file(self, input_file):
        self.log_event(f"Input File: {input_file}")

    """
    logs the user input/responses
    @param user_input
    """

    def log_user_input(self, user_input):
        self.log_event(f"User Input/Response: {user_input}")