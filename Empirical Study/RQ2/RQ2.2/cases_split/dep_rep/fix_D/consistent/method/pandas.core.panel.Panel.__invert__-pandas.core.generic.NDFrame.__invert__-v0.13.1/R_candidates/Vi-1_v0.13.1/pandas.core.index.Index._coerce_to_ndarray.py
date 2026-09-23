    @classmethod
    def _coerce_to_ndarray(cls, data):
        """coerces data to ndarray, raises on scalar data. Converts other
        iterables to list first and then to array. Does not touch ndarrays."""

        if not isinstance(data, np.ndarray):
            if np.isscalar(data):
                cls._scalar_data_error(data)

            # other iterable of some kind
            if not isinstance(data, (ABCSeries, list, tuple)):
                data = list(data)
            data = np.asarray(data)
        return data
