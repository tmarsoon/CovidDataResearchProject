from edu.upenn.cit594.logging import Logger

class FileSuperLogger:
    """
    Unlike the solo project,
    """
    def __init__(self, filename, logger: Logger):
        # creating two variables with protected as the data type so we can access these within other classes of the same package
        self._filename = filename
        self._logger = logger
    def open_logger(self):
        """
        Calling the changeOutPutDest method from Logger class
        @param openLogger
        """
        if self._logger is None:
            return
        self._logger.change_output_dest(self._filename)