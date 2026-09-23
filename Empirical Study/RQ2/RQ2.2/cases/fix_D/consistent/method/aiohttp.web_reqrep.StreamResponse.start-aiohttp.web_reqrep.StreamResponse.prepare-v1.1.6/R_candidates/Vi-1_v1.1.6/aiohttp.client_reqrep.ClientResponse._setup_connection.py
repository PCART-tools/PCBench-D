    def _setup_connection(self, connection):
        self._reader = connection.reader
        self._connection = connection
        self.content = self.flow_control_class(
            connection.reader, loop=connection.loop, timeout=self._timeout)
