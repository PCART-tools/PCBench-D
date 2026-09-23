    @property
    def flags(self):
        """
        Return the ndarray.flags for the underlying data.
        """
        warnings.warn("{obj}.flags is deprecated and will be removed "
                      "in a future version".format(obj=type(self).__name__),
                      FutureWarning, stacklevel=2)
        return self.values.flags
