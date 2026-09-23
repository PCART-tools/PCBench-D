    def _maybe_cast_slice_bound(self, label, side: str, kind: str):
        """
        If label is a string or a datetime, cast it to Period.ordinal according
        to resolution.

        Parameters
        ----------
        label : object
        side : {'left', 'right'}
        kind : {'loc', 'getitem'}

        Returns
        -------
        bound : Period or object

        Notes
        -----
        Value of `side` parameter should be validated in caller.

        """
        assert kind in ["loc", "getitem"]

        if isinstance(label, datetime):
            return Period(label, freq=self.freq)
        elif isinstance(label, str):
            try:
                parsed, reso = parse_time_string(label, self.freq)
                reso = Resolution.from_attrname(reso)
                bounds = self._parsed_string_to_bounds(reso, parsed)
                return bounds[0 if side == "left" else 1]
            except ValueError as err:
                # string cannot be parsed as datetime-like
                raise self._invalid_indexer("slice", label) from err
        elif is_integer(label) or is_float(label):
            raise self._invalid_indexer("slice", label)

        return label
