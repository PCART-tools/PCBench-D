    def _maybe_cast_slice_bound(self, label, side: str, kind):
        """
        If label is a string, cast it to datetime according to resolution.

        Parameters
        ----------
        label : object
        side : {'left', 'right'}
        kind : {'loc', 'getitem'} or None

        Returns
        -------
        label : object

        Notes
        -----
        Value of `side` parameter should be validated in caller.
        """
        assert kind in ["loc", "getitem", None]

        if isinstance(label, str):
            freq = getattr(self, "freqstr", getattr(self, "inferred_freq", None))
            try:
                parsed, reso = parsing.parse_time_string(label, freq)
            except parsing.DateParseError as err:
                raise self._invalid_indexer("slice", label) from err

            reso = Resolution.from_attrname(reso)
            lower, upper = self._parsed_string_to_bounds(reso, parsed)
            # lower, upper form the half-open interval:
            #   [parsed, parsed + 1 freq)
            # because label may be passed to searchsorted
            # the bounds need swapped if index is reverse sorted and has a
            # length > 1 (is_monotonic_decreasing gives True for empty
            # and length 1 index)
            if self._is_strictly_monotonic_decreasing and len(self) > 1:
                return upper if side == "left" else lower
            return lower if side == "left" else upper
        elif isinstance(label, (self._data._recognized_scalars, date)):
            self._deprecate_mismatched_indexing(label)
        else:
            raise self._invalid_indexer("slice", label)

        return self._maybe_cast_for_get_loc(label)
