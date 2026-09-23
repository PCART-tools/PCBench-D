    def get_loc(self, key, method=None, tolerance=None):
        """
        Get integer location for requested label

        Returns
        -------
        loc : int
        """
        self._check_indexing_error(key)

        orig_key = key
        if is_valid_na_for_dtype(key, self.dtype):
            key = NaT

        if isinstance(key, self._data._recognized_scalars):
            # needed to localize naive datetimes
            self._deprecate_mismatched_indexing(key)
            key = self._maybe_cast_for_get_loc(key)

        elif isinstance(key, str):

            try:
                parsed, reso = self._parse_with_reso(key)
            except ValueError as err:
                raise KeyError(key) from err
            self._deprecate_mismatched_indexing(parsed, one_way=True)

            if self._can_partial_date_slice(reso):
                try:
                    return self._partial_date_slice(reso, parsed)
                except KeyError as err:
                    if method is None:
                        raise KeyError(key) from err

            key = self._maybe_cast_for_get_loc(key)

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
