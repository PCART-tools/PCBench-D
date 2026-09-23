    def __array__(self, dtype=None):
        """
        the array interface, return my values
        We return an object array here to preserve our scalar values
        """
        return self._coerce_to_ndarray()
