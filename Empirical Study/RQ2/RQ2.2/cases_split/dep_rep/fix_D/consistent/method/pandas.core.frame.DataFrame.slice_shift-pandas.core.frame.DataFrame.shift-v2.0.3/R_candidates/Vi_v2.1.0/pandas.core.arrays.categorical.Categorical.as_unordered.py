    def as_unordered(self) -> Self:
        """
        Set the Categorical to be unordered.

        Returns
        -------
        Categorical
            Unordered Categorical.

        Examples
        --------
        For :class:`pandas.Series`:

        >>> raw_cat = pd.Categorical(['a', 'b', 'c', 'a'], ordered=True)
        >>> ser = pd.Series(raw_cat)
        >>> ser.cat.ordered
        True
        >>> ser = ser.cat.as_unordered()
        >>> ser.cat.ordered
        False

        For :class:`pandas.CategoricalIndex`:

        >>> ci = pd.CategoricalIndex(['a', 'b', 'c', 'a'], ordered=True)
        >>> ci.ordered
        True
        >>> ci = ci.as_unordered()
        >>> ci.ordered
        False
        """
        return self.set_ordered(False)
