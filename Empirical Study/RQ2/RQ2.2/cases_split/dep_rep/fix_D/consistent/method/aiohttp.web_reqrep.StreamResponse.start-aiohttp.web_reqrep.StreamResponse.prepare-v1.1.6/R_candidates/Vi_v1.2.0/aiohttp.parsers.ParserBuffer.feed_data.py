    def feed_data(self, data):
        if not self._helper.exception:
            self._writer.send(data)
