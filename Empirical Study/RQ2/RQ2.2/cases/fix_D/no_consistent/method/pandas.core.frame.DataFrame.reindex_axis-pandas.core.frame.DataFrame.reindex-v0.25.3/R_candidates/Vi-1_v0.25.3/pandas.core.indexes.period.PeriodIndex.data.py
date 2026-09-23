    @property
    def data(self):
        """ return the data pointer of the underlying data """
        warnings.warn(
            "{obj}.data is deprecated and will be removed "
            "in a future version".format(obj=type(self).__name__),
            FutureWarning,
            stacklevel=2,
        )
        return np.asarray(self._data).data
