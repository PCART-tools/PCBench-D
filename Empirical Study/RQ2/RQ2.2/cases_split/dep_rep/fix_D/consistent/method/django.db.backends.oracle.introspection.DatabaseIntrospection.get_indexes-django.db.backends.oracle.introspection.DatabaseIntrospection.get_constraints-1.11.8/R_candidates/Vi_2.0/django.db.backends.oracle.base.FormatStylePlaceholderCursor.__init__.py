    def __init__(self, connection):
        self.cursor = connection.cursor()
        self.cursor.outputtypehandler = self._output_type_handler
        # The default for cx_Oracle < 5.3 is 50.
        self.cursor.arraysize = 100
