    @offset.setter
    def offset(self, value):
        """get/set the frequency of the Index"""
        msg = ('DatetimeIndex.offset has been deprecated and will be removed '
               'in a future version; use DatetimeIndex.freq instead.')
        warnings.warn(msg, FutureWarning, stacklevel=2)
        self.freq = value
