    def _maybe_cast_slice_bound(self, label, side: str_t):
        """
        This function should be overloaded in subclasses that allow non-trivial
        casting on label-slice bounds, e.g. datetime-like indices allowing
        strings containing formatted datetimes.

        Parameters
        ----------
        label : object
        side : {'left', 'right'}

        Returns
        -------
        label : object

        Notes
        -----
        Value of `side` parameter should be validated in caller.
        """

        # We are a plain index here (sub-class override this method if they
        # wish to have special treatment for floats/ints, e.g. datetimelike Indexes

        if is_numeric_dtype(self.dtype):
            return self._maybe_cast_indexer(label)

        # reject them, if index does not contain label
        if (is_float(label) or is_integer(label)) and label not in self:
            self._raise_invalid_indexer("slice", label)

        return label
