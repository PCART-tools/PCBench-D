    def _shallow_copy(self, values=None, **kwargs):
        # TODO: simplify, figure out type of values
        if values is None:
            values = self._data

        if isinstance(values, type(self)):
            values = values._values

        if not isinstance(values, PeriodArray):
            if isinstance(values, np.ndarray) and is_integer_dtype(values.dtype):
                values = PeriodArray(values, freq=self.freq)
            else:
                # in particular, I would like to avoid period_array here.
                # Some people seem to be calling use with unexpected types
                # Index.difference -> ndarray[Period]
                # DatetimelikeIndexOpsMixin.repeat -> ndarray[ordinal]
                # I think that once all of Datetime* are EAs, we can simplify
                # this quite a bit.
                values = period_array(values, freq=self.freq)

        # We don't allow changing `freq` in _shallow_copy.
        validate_dtype_freq(self.dtype, kwargs.get("freq"))
        attributes = self._get_attributes_dict()

        attributes.update(kwargs)
        if not len(values) and "dtype" not in kwargs:
            attributes["dtype"] = self.dtype
        return self._simple_new(values, **attributes)
