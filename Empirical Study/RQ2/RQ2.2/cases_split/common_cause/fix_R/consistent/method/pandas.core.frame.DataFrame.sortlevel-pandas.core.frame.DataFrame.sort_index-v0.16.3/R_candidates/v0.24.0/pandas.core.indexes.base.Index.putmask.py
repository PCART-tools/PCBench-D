    def putmask(self, mask, value):
        """
        Return a new Index of the values set with the mask.

        See Also
        --------
        numpy.ndarray.putmask
        """
        values = self.values.copy()
        try:
            np.putmask(values, mask, self._convert_for_op(value))
            return self._shallow_copy(values)
        except (ValueError, TypeError) as err:
            if is_object_dtype(self):
                raise err

            # coerces to object
            return self.astype(object).putmask(mask, value)
