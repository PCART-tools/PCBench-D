    def putmask(self, mask, value):
        """
        return a new Index of the values set with the mask

        See also
        --------
        numpy.ndarray.putmask
        """
        values = self.values.copy()
        try:
            np.putmask(values, mask, self._convert_for_op(value))
            return self._shallow_copy(values)
        except (ValueError, TypeError):
            # coerces to object
            return self.astype(object).putmask(mask, value)
