    def _sanitize_column(self, value) -> tuple[ArrayLike, BlockValuesRefs | None]:
        """
        Ensures new columns (which go into the BlockManager as new blocks) are
        always copied (or a reference is being tracked to them under CoW)
        and converted into an array.

        Parameters
        ----------
        value : scalar, Series, or array-like

        Returns
        -------
        tuple of numpy.ndarray or ExtensionArray and optional BlockValuesRefs
        """
        self._ensure_valid_index(value)

        # Using a DataFrame would mean coercing values to one dtype
        assert not isinstance(value, DataFrame)
        if is_dict_like(value):
            if not isinstance(value, Series):
                value = Series(value)
            return _reindex_for_setitem(value, self.index)

        if is_list_like(value):
            com.require_length_match(value, self.index)
        return sanitize_array(value, self.index, copy=True, allow_2d=True), None
