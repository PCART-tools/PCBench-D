    def data_received(self, data):
        super().data_received(data)

        # reading request
        if not self._reading_request:
            self._reading_request = True
