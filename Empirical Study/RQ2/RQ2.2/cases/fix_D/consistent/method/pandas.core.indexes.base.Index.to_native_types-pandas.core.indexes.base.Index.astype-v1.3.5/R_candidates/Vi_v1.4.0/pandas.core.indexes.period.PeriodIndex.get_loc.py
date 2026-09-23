    def get_loc(self, key, method=None, tolerance=None):
        """
        Get integer location for requested label.

        Parameters
        ----------
        key : Period, NaT, str, or datetime
            String or datetime key must be parsable as Period.

        Returns
        -------
        loc : int or ndarray[int64]

        Raises
        ------
        KeyError
            Key is not present in the index.
        TypeError
            If key is listlike or otherwise not hashable.
        """
        orig_key = key

        self._check_indexing_error(key)

        if is_valid_na_for_dtype(key, self.dtype):
            key = NaT

        elif isinstance(key, str):

            try:
                parsed, reso = self._parse_with_reso(key)
            except ValueError as err:
                # A string with invalid format
                raise KeyError(f"Cannot interpret '{key}' as period") from err

            if self._can_partial_date_slice(reso):
                try:
                    return self._partial_date_slice(reso, parsed)
                except KeyError as err:
                    # TODO: pass if method is not None, like DTI does?
                    raise KeyError(key) from err

            if reso == self.dtype.resolution:
                # the reso < self.dtype.resolution case goes through _get_string_slice
                key = Period(parsed, freq=self.freq)
                loc = self.get_loc(key, method=method, tolerance=tolerance)
                # Recursing instead of falling through matters for the exception
                #  message in test_get_loc3 (though not clear if that really matters)
                return loc
            elif method is None:
                raise KeyError(key)
            else:
                key = Period(parsed, freq=self.freq)

        elif isinstance(key, Period):
            sfreq = self.freq
            kfreq = key.freq
            if not (
                sfreq.n == kfreq.n
                and sfreq._period_dtype_code == kfreq._period_dtype_code
            ):
                # GH#42247 For the subset of DateOffsets that can be Period freqs,
                #  checking these two attributes is sufficient to check equality,
                #  and much more performant than `self.freq == key.freq`
                raise KeyError(key)
        elif isinstance(key, datetime):
            try:
                key = Period(key, freq=self.freq)
            except ValueError as err:
                # we cannot construct the Period
                raise KeyError(orig_key) from err
        else:
            # in particular integer, which Period constructor would cast to string
            raise KeyError(key)

        try:
            return Index.get_loc(self, key, method, tolerance)
        except KeyError as err:
            raise KeyError(orig_key) from err
