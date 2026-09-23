    def factorize(self, na_sentinel=-1):
        # type: (int) -> Tuple[ndarray, ExtensionArray]
        """
        Encode the extension array as an enumerated type.

        Parameters
        ----------
        na_sentinel : int, default -1
            Value to use in the `labels` array to indicate missing values.

        Returns
        -------
        labels : ndarray
            An integer NumPy array that's an indexer into the original
            ExtensionArray.
        uniques : ExtensionArray
            An ExtensionArray containing the unique values of `self`.

            .. note::

               uniques will *not* contain an entry for the NA value of
               the ExtensionArray if there are any missing values present
               in `self`.

        See Also
        --------
        pandas.factorize : Top-level factorize method that dispatches here.

        Notes
        -----
        :meth:`pandas.factorize` offers a `sort` keyword as well.
        """
        # Impelmentor note: There are two ways to override the behavior of
        # pandas.factorize
        # 1. _values_for_factorize and _from_factorize.
        #    Specify the values passed to pandas' internal factorization
        #    routines, and how to convert from those values back to the
        #    original ExtensionArray.
        # 2. ExtensionArray.factorize.
        #    Complete control over factorization.
        from pandas.core.algorithms import _factorize_array

        arr, na_value = self._values_for_factorize()

        labels, uniques = _factorize_array(arr, na_sentinel=na_sentinel,
                                           na_value=na_value)

        uniques = self._from_factorized(uniques, self)
        return labels, uniques
