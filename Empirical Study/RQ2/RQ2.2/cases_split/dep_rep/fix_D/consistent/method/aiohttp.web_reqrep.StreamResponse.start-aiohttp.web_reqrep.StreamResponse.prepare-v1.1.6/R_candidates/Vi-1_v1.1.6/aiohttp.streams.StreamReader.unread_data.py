    def unread_data(self, data):
        """ rollback reading some data from stream, inserting it to buffer head.
        """
        if not data:
            return

        if self._buffer_offset:
            self._buffer[0] = self._buffer[0][self._buffer_offset:]
            self._buffer_offset = 0
        self._buffer.appendleft(data)
        self._buffer_size += len(data)
