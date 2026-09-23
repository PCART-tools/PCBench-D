    def take_nd(self, indexer, allow_fill=None, fill_value=None):
        """
        Take elements from the Categorical.

        Parameters
        ----------
        indexer : sequence of integers
        allow_fill : bool, default None.
            How to handle negative values in `indexer`.

            * False: negative values in `indices` indicate positional indices
              from the right. This is similar to
              :func:`numpy.take`.

            * True: negative values in `indices` indicate missing values
              (the default). These values are set to `fill_value`. Any other
              other negative values raise a ``ValueError``.

            .. versionchanged:: 0.23.0

               Deprecated the default value of `allow_fill`. The deprecated
               default is ``True``. In the future, this will change to
               ``False``.

        Returns
        -------
        Categorical
            This Categorical will have the same categories and ordered as
            `self`.
        """
        indexer = np.asarray(indexer, dtype=np.intp)
        if allow_fill is None:
            if (indexer < 0).any():
                warn(_take_msg, FutureWarning, stacklevel=2)
                allow_fill = True

        if isna(fill_value):
            # For categorical, any NA value is considered a user-facing
            # NA value. Our storage NA value is -1.
            fill_value = -1

        codes = take(self._codes, indexer, allow_fill=allow_fill,
                     fill_value=fill_value)
        result = self._constructor(codes, categories=self.categories,
                                   ordered=self.ordered, fastpath=True)
        return result
