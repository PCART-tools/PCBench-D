    def _coerce_to_ndarray(self):
        """
        coerce to an ndarary of object dtype
        """

        # TODO(jreback) make this better
        data = self._data.astype(object)
        data[self._mask] = self._na_value
        return data
