    def _values_for_argsort(self) -> np.ndarray:
        """
        Return values for sorting.

        Returns
        -------
        ndarray
            The transformed values should maintain the ordering between values
            within the array.

        See Also
        --------
        ExtensionArray.argsort : Return the indices that would sort this array.

        Notes
        -----
        The caller is responsible for *not* modifying these values in-place, so
        it is safe for implementors to give views on `self`.

        Functions that use this (e.g. ExtensionArray.argsort) should ignore
        entries with missing values in the original array (according to `self.isna()`).
        This means that the corresponding entries in the returned array don't need to
        be modified to sort correctly.
        """
        # Note: this is used in `ExtensionArray.argsort/argmin/argmax`.
        return np.array(self)
