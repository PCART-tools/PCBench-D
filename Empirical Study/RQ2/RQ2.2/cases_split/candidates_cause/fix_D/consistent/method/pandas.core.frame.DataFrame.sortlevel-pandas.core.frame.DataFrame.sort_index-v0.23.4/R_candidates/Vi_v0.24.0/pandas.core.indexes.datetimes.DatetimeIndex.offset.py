    @offset.setter
    def offset(self, value):
        """
        get/set the frequency of the instance
        """
        msg = ('{cls}.offset has been deprecated and will be removed '
               'in a future version; use {cls}.freq instead.'
               .format(cls=type(self).__name__))
        warnings.warn(msg, FutureWarning, stacklevel=2)
        self.freq = value
