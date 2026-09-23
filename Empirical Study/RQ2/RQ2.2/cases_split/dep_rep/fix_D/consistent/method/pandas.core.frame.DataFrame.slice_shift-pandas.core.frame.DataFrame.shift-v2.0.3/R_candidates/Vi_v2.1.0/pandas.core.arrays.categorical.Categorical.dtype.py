    @property
    def dtype(self) -> CategoricalDtype:
        """
        The :class:`~pandas.api.types.CategoricalDtype` for this instance.

        Examples
        --------
        >>> cat = pd.Categorical(['a', 'b'], ordered=True)
        >>> cat
        ['a', 'b']
        Categories (2, object): ['a' < 'b']
        >>> cat.dtype
        CategoricalDtype(categories=['a', 'b'], ordered=True, categories_dtype=object)
        """
        return self._dtype
