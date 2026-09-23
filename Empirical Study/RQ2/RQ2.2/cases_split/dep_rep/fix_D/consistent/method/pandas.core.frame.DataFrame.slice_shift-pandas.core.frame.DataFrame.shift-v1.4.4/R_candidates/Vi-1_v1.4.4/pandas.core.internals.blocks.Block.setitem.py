    def setitem(self, indexer, value):
        """
        Attempt self.values[indexer] = value, possibly creating a new array.

        Parameters
        ----------
        indexer : tuple, list-like, array-like, slice, int
            The subset of self.values to set
        value : object
            The value being set

        Returns
        -------
        Block

        Notes
        -----
        `indexer` is a direct slice/positional indexer. `value` must
        be a compatible shape.
        """
        transpose = self.ndim == 2

        if isinstance(indexer, np.ndarray) and indexer.ndim > self.ndim:
            raise ValueError(f"Cannot set values with ndim > {self.ndim}")

        # coerce None values, if appropriate
        if value is None:
            if self.is_numeric:
                value = np.nan

        # coerce if block dtype can store value
        values = cast(np.ndarray, self.values)
        if not self._can_hold_element(value):
            # current dtype cannot store value, coerce to common dtype
            return self.coerce_to_target_dtype(value).setitem(indexer, value)

        # value must be storable at this moment
        if is_extension_array_dtype(getattr(value, "dtype", None)):
            # We need to be careful not to allow through strings that
            #  can be parsed to EADtypes
            arr_value = value
        else:
            arr_value = np.asarray(value)

        if transpose:
            values = values.T

        # length checking
        check_setitem_lengths(indexer, value, values)

        if is_empty_indexer(indexer, arr_value):
            # GH#8669 empty indexers, test_loc_setitem_boolean_mask_allfalse
            pass

        elif is_scalar_indexer(indexer, self.ndim):
            # setting a single element for each dim and with a rhs that could
            #  be e.g. a list; see GH#6043
            values[indexer] = value

        else:
            value = setitem_datetimelike_compat(values, len(values[indexer]), value)
            values[indexer] = value

        return self
