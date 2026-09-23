    @final
    def get_value(self, series: Series, key):
        """
        Fast lookup of value from 1-dimensional ndarray.

        Only use this if you know what you're doing.

        Returns
        -------
        scalar or Series
        """
        warnings.warn(
            "get_value is deprecated and will be removed in a future version. "
            "Use Series[key] instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )

        self._check_indexing_error(key)

        try:
            # GH 20882, 21257
            # First try to convert the key to a location
            # If that fails, raise a KeyError if an integer
            # index, otherwise, see if key is an integer, and
            # try that
            loc = self.get_loc(key)
        except KeyError:
            if not self._should_fallback_to_positional:
                raise
            elif is_integer(key):
                # If the Index cannot hold integer, then this is unambiguously
                #  a locational lookup.
                loc = key
            else:
                raise

        return self._get_values_for_loc(series, loc, key)
