    def __init__(self, connection):
        self.cursor = connection.cursor()
        self.cursor.outputtypehandler = self._output_type_handler
        # Default arraysize of 1 is highly sub-optimal.
        self.cursor.arraysize = 100
