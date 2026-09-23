    def data_received(self, data):
        super().data_received(data)

        # we can not gracefully shutdown handler
        # if we in process of reading request
        self._reading_request = True
