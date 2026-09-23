    def _sanitize_column(self, key, value, **kwargs):
        """
        Creates a new SparseArray from the input value.

        Parameters
        ----------
        key : object
        value : scalar, Series, or array-like
        kwargs : dict

        Returns
        -------
        sanitized_column : SparseArray

        """
        def sp_maker(x, index=None):
            return SparseArray(x, index=index,
                               fill_value=self._default_fill_value,
                               kind=self._default_kind)
        if isinstance(value, SparseSeries):
            clean = value.reindex(self.index).as_sparse_array(
                fill_value=self._default_fill_value, kind=self._default_kind)

        elif isinstance(value, SparseArray):
            if len(value) != len(self.index):
                raise AssertionError('Length of values does not match '
                                     'length of index')
            clean = value

        elif hasattr(value, '__iter__'):
            if isinstance(value, Series):
                clean = value.reindex(self.index)
                if not isinstance(value, SparseSeries):
                    clean = sp_maker(clean)
            else:
                if len(value) != len(self.index):
                    raise AssertionError('Length of values does not match '
                                         'length of index')
                clean = sp_maker(value)

        # Scalar
        else:
            clean = sp_maker(value, self.index)

        # always return a SparseArray!
        return clean
