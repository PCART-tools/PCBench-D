    @property
    def ordered(self) -> Ordered:
        """
        Whether the categories have an ordered relationship.

        Examples
        --------
        For :class:`pandas.Series`:

        >>> ser = pd.Series(['a', 'b', 'c', 'a'], dtype='category')
        >>> ser.cat.ordered
        False

        >>> raw_cat = pd.Categorical(['a', 'b', 'c', 'a'], ordered=True)
        >>> ser = pd.Series(raw_cat)
        >>> ser.cat.ordered
        True

        For :class:`pandas.Categorical`:

        >>> cat = pd.Categorical(['a', 'b'], ordered=True)
        >>> cat.ordered
        True

        >>> cat = pd.Categorical(['a', 'b'], ordered=False)
        >>> cat.ordered
        False

        For :class:`pandas.CategoricalIndex`:

        >>> ci = pd.CategoricalIndex(['a', 'b'], ordered=True)
        >>> ci.ordered
        True

        >>> ci = pd.CategoricalIndex(['a', 'b'], ordered=False)
        >>> ci.ordered
        False
        """
        return self.dtype.ordered
