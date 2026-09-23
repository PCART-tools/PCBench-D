    def factorize(
        self,
        na_sentinel: int | lib.NoDefault = lib.no_default,
        use_na_sentinel: bool | lib.NoDefault = lib.no_default,
    ) -> tuple[np.ndarray, ExtensionArray]:
        """
        Encode the extension array as an enumerated type.

        Parameters
        ----------
        na_sentinel : int, default -1
            Value to use in the `codes` array to indicate missing values.

            .. deprecated:: 1.5.0
                The na_sentinel argument is deprecated and
                will be removed in a future version of pandas. Specify use_na_sentinel
                as either True or False.

        use_na_sentinel : bool, default True
            If True, the sentinel -1 will be used for NaN values. If False,
            NaN values will be encoded as non-negative integers and will not drop the
            NaN from the uniques of the values.

            .. versionadded:: 1.5.0

        Returns
        -------
        codes : ndarray
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
        factorize : Top-level factorize method that dispatches here.

        Notes
        -----
        :meth:`pandas.factorize` offers a `sort` keyword as well.
        """
        # Implementer note: There are two ways to override the behavior of
        # pandas.factorize
        # 1. _values_for_factorize and _from_factorize.
        #    Specify the values passed to pandas' internal factorization
        #    routines, and how to convert from those values back to the
        #    original ExtensionArray.
        # 2. ExtensionArray.factorize.
        #    Complete control over factorization.
        resolved_na_sentinel = resolve_na_sentinel(na_sentinel, use_na_sentinel)
        arr, na_value = self._values_for_factorize()

        codes, uniques = factorize_array(
            arr, na_sentinel=resolved_na_sentinel, na_value=na_value
        )

        uniques_ea = self._from_factorized(uniques, self)
        return codes, uniques_ea
