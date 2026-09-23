    def __init__(self, connection):
        self.cursor = connection.cursor()
        self.cursor.outputtypehandler = self._output_type_handler
