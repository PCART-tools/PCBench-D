    @property
    def itemsize(self):
        """
        Return the size of the dtype of the item of the underlying data.
        """
        warnings.warn("{obj}.itemsize is deprecated and will be removed "
                      "in a future version".format(obj=type(self).__name__),
                      FutureWarning, stacklevel=2)
        return self._ndarray_values.itemsize
