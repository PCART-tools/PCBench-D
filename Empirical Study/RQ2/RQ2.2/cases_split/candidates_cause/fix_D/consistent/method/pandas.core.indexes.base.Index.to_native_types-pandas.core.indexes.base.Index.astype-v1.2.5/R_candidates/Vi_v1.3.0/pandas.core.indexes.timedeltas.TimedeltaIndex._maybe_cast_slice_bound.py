    def _maybe_cast_slice_bound(self, label, side: str, kind=lib.no_default):
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
        assert kind in ["loc", "getitem", None, lib.no_default]
        self._deprecated_arg(kind, "kind", "_maybe_cast_slice_bound")

        if isinstance(label, str):
            try:
                parsed = Timedelta(label)
            except ValueError as err:
                # e.g. 'unit abbreviation w/o a number'
                raise self._invalid_indexer("slice", label) from err

            # The next two lines are analogous to DTI/PI._parsed_str_to_bounds
            lower = parsed.round(parsed.resolution_string)
            upper = lower + to_offset(parsed.resolution_string) - Timedelta(1, "ns")
            return lower if side == "left" else upper
        elif not isinstance(label, self._data._recognized_scalars):
            raise self._invalid_indexer("slice", label)

        return label
