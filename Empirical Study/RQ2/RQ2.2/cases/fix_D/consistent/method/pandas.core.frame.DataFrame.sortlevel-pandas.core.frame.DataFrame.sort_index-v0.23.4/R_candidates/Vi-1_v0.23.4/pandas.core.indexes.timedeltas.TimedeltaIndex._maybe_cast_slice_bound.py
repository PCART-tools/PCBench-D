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
        assert kind in ['ix', 'loc', 'getitem', None]

        if isinstance(label, compat.string_types):
            parsed = _coerce_scalar_to_timedelta_type(label, box=True)
            lbound = parsed.round(parsed.resolution)
            if side == 'left':
                return lbound
            else:
                return (lbound + to_offset(parsed.resolution) -
                        Timedelta(1, 'ns'))
        elif ((is_integer(label) or is_float(label)) and
              not is_timedelta64_dtype(label)):
            self._invalid_indexer('slice', label)

        return label
