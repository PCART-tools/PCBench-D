    def _maybe_cast_slice_bound(self, label, side: str, kind=lib.no_default):
        """
        If label is a string or a datetime, cast it to Period.ordinal according
        to resolution.

        Parameters
        ----------
        label : object
        side : {'left', 'right'}
        kind : {'loc', 'getitem'}, or None

        Returns
        -------
        bound : Period or object

        Notes
        -----
        Value of `side` parameter should be validated in caller.

        """
        assert kind in ["loc", "getitem", None, lib.no_default]
        self._deprecated_arg(kind, "kind", "_maybe_cast_slice_bound")

        if isinstance(label, datetime):
            return Period(label, freq=self.freq)
        elif isinstance(label, str):
            try:
                parsed, reso_str = parse_time_string(label, self.freq)
            except ValueError as err:
                # string cannot be parsed as datetime-like
                raise self._invalid_indexer("slice", label) from err

            reso = Resolution.from_attrname(reso_str)
            lower, upper = self._parsed_string_to_bounds(reso, parsed)
            return lower if side == "left" else upper
        elif not isinstance(label, self._data._recognized_scalars):
            raise self._invalid_indexer("slice", label)

        return label
