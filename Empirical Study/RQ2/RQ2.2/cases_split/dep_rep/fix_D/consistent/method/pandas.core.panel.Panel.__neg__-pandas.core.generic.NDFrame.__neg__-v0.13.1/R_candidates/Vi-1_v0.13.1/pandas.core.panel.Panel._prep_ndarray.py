    @staticmethod
    def _prep_ndarray(self, values, copy=True):
        if not isinstance(values, np.ndarray):
            values = np.asarray(values)
            # NumPy strings are a pain, convert to object
            if issubclass(values.dtype.type, compat.string_types):
                values = np.array(values, dtype=object, copy=True)
        else:
            if copy:
                values = values.copy()
        if values.ndim != self._AXIS_LEN:
            raise ValueError("The number of dimensions required is {0}, "
                             "but the number of dimensions of the "
                             "ndarray given was {1}".format(self._AXIS_LEN,
                                                            values.ndim))
        return values
