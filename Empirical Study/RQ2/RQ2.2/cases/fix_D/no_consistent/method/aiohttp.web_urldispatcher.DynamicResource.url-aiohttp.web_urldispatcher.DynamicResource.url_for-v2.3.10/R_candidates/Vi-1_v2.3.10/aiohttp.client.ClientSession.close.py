    def close(self):
        """Close underlying connector.

        Release all acquired resources.
        """
        if not self.closed:
            if self._connector_owner:
                self._connector.close()
            self._connector = None

        return deprecated_noop('ClientSession.close() is a coroutine')
