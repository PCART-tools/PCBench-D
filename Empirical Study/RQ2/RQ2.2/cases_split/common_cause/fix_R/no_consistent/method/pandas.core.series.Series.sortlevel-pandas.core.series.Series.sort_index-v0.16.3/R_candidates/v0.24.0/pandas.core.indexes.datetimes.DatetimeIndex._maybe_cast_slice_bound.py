    def _maybe_cast_slice_bound(self, label, side, kind):
        """
        If label is a string, cast it to datetime according to resolution.

        Parameters
        ----------
        label : object
        side : {'left', 'right'}
        kind : {'ix', 'loc', 'getitem'}

        Returns
        -------
        label :  object

        Notes
        -----
        Value of `side` parameter should be validated in caller.

        """
        assert kind in ['ix', 'loc', 'getitem', None]

        if is_float(label) or isinstance(label, time) or is_integer(label):
            self._invalid_indexer('slice', label)

        if isinstance(label, compat.string_types):
            freq = getattr(self, 'freqstr',
                           getattr(self, 'inferred_freq', None))
            _, parsed, reso = parsing.parse_time_string(label, freq)
            lower, upper = self._parsed_string_to_bounds(reso, parsed)
            # lower, upper form the half-open interval:
            #   [parsed, parsed + 1 freq)
            # because label may be passed to searchsorted
            # the bounds need swapped if index is reverse sorted and has a
            # length > 1 (is_monotonic_decreasing gives True for empty
            # and length 1 index)
            if self._is_strictly_monotonic_decreasing and len(self) > 1:
                return upper if side == 'left' else lower
            return lower if side == 'left' else upper
        else:
            return label
