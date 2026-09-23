    def putmask(self, mask, value) -> Index:
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
        mask, noop = validate_putmask(self._values, mask)
        if noop:
            return self.copy()

        if value is None and (self._is_numeric_dtype or self.dtype == object):
            value = self._na_value
        try:
            converted = self._validate_fill_value(value)
        except (ValueError, TypeError) as err:
            if is_object_dtype(self):
                raise err

            dtype = self._find_common_type_compat(value)
            return self.astype(dtype).putmask(mask, value)

        values = self._values.copy()
        # error: Argument 1 to "setitem_datetimelike_compat" has incompatible type
        # "Union[ExtensionArray, ndarray]"; expected "ndarray"
        converted = setitem_datetimelike_compat(
            values, mask.sum(), converted  # type: ignore[arg-type]
        )
        np.putmask(values, mask, converted)

        return type(self)._simple_new(values, name=self.name)
