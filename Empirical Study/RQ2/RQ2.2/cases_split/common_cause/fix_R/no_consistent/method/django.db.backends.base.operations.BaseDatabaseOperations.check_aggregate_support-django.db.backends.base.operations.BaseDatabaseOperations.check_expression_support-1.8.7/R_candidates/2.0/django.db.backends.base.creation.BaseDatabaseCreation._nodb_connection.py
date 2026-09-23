    @property
    def _nodb_connection(self):
        """
        Used to be defined here, now moved to DatabaseWrapper.
        """
        return self.connection._nodb_connection
