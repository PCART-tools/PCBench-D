    def _maybe_cast_slice_bound(self, label, side: str, kind):
        """
        If label is a string, cast it to timedelta according to resolution.

        Parameters
        ----------
        label : object
        side : {'left', 'right'}
        kind : {'loc', 'getitem'} or None

        Returns
        -------
        label : object
        """
        assert kind in ["loc", "getitem", None]

        if isinstance(label, str):
            parsed = Timedelta(label)
            lbound = parsed.round(parsed.resolution_string)
            if side == "left":
                return lbound
            else:
                return lbound + to_offset(parsed.resolution_string) - Timedelta(1, "ns")
        elif not isinstance(label, self._data._recognized_scalars):
            raise self._invalid_indexer("slice", label)

        return label
