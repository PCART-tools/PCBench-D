    def get_loc(self, key, method=None, tolerance=None):
        """
        Get integer location for requested label

        Returns
        -------
        loc : int
        """
        if not is_scalar(key):
            raise InvalidIndexError(key)

        orig_key = key
        if is_valid_nat_for_dtype(key, self.dtype):
            key = NaT

        if isinstance(key, self._data._recognized_scalars):
            # needed to localize naive datetimes
            self._deprecate_mismatched_indexing(key)
            key = self._maybe_cast_for_get_loc(key)

        elif isinstance(key, str):
            try:
                return self._get_string_slice(key)
            except (TypeError, KeyError, ValueError, OverflowError):
                pass

            try:
                key = self._maybe_cast_for_get_loc(key)
            except ValueError as err:
                raise KeyError(key) from err

        elif isinstance(key, timedelta):
            # GH#20464
            raise TypeError(
                f"Cannot index {type(self).__name__} with {type(key).__name__}"
            )

        elif isinstance(key, time):
            if method is not None:
                raise NotImplementedError(
                    "cannot yet lookup inexact labels when key is a time object"
                )
            return self.indexer_at_time(key)

        else:
            # unrecognized type
            raise KeyError(key)

        try:
            return Index.get_loc(self, key, method, tolerance)
        except KeyError as err:
            raise KeyError(orig_key) from err
