    @classmethod
    def _coerce_to_ndarray(cls, data):
        """
        Coerces data to ndarray.

        Converts other iterables to list first and then to array.
        Does not touch ndarrays.

        Raises
        ------
        TypeError
            When the data passed in is a scalar.
        """

        if not isinstance(data, (np.ndarray, Index)):
            if data is None or is_scalar(data):
                cls._scalar_data_error(data)

            # other iterable of some kind
            if not isinstance(data, (ABCSeries, list, tuple)):
                data = list(data)
            data = np.asarray(data)
        return data
