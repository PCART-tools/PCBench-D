    def _maybe_cast_slice_bound(self, label, side, kind):
        """
        If label is a string, cast it to timedelta according to resolution.


        Parameters
        ----------
        label : object
        side : {'left', 'right'}
        kind : {'ix', 'loc', 'getitem'}

        Returns
        -------
        label :  object

        """
        assert kind in ["ix", "loc", "getitem", None]

        if isinstance(label, str):
            parsed = Timedelta(label)
            lbound = parsed.round(parsed.resolution_string)
            if side == "left":
                return lbound
            else:
                return lbound + to_offset(parsed.resolution_string) - Timedelta(1, "ns")
        elif is_integer(label) or is_float(label):
            self._invalid_indexer("slice", label)

        return label
