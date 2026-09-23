    def external_values(self):
        """ we internally represent the data as a DatetimeIndex, but for
        external compat with ndarray, export as a ndarray of Timestamps
        """
        return self.values.astype('datetime64[ns]').values
