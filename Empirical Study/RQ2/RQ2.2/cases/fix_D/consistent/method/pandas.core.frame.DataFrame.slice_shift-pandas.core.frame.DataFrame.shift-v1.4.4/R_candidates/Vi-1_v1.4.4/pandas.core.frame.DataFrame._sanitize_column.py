    def _sanitize_column(self, value) -> ArrayLike:
        """
        Ensures new columns (which go into the BlockManager as new blocks) are
        always copied and converted into an array.

        Parameters
        ----------
        value : scalar, Series, or array-like

        Returns
        -------
        numpy.ndarray or ExtensionArray
        """
        self._ensure_valid_index(value)

        # We can get there through loc single_block_path
        if isinstance(value, (DataFrame, Series)):
            return _reindex_for_setitem(value, self.index)

        if is_list_like(value):
            com.require_length_match(value, self.index)
        return sanitize_array(value, self.index, copy=True, allow_2d=True)
