    def _maybe_cast_slice_bound(self, label, side, kind):
        """
        This function should be overloaded in subclasses that allow non-trivial
        casting on label-slice bounds, e.g. datetime-like indices allowing
        strings containing formatted datetimes.

        Parameters
        ----------
        label : object
        side : {'left', 'right'}
        kind : string / None

        Returns
        -------
        label :  object

        Notes
        -----
        Value of `side` parameter should be validated in caller.

        """

        # we are a numeric index, so we accept
        # integer/floats directly
        if not (is_integer(label) or is_float(label)):
            self._invalid_indexer('slice',label)

        return label
