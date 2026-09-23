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

        # We are a plain index here (sub-class override this method if they
        # wish to have special treatment for floats/ints, e.g. Float64Index and
        # datetimelike Indexes
        # reject them
        if is_float(label):
            self._invalid_indexer('slice',label)

        # we are trying to find integer bounds on a non-integer based index
        # this is rejected (generally .loc gets you here)
        elif is_integer(label):
            self._invalid_indexer('slice',label)

        return label
