    def putmask(self, mask, value):
        """
        Return a new Index of the values set with the mask.

        Returns
        -------
        Index

        See Also
        --------
        numpy.ndarray.putmask : Changes elements of an array
            based on conditional and input values.
        """
        values = self._values.copy()
        try:
            converted = self._validate_fill_value(value)
        except (ValueError, TypeError) as err:
            if is_object_dtype(self):
                raise err

            # coerces to object
            return self.astype(object).putmask(mask, value)

        np.putmask(values, mask, converted)
        return self._shallow_copy(values)
