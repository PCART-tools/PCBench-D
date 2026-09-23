    def to_frame(
        self, index: bool = True, name: Hashable = lib.no_default
    ) -> DataFrame:
        """
        Create a DataFrame with a column containing the Index.

        Parameters
        ----------
        index : bool, default True
            Set the index of the returned DataFrame as the original Index.

        name : object, default None
            The passed name should substitute for the index name (if it has
            one).

        Returns
        -------
        DataFrame
            DataFrame containing the original Index data.

        See Also
        --------
        Index.to_series : Convert an Index to a Series.
        Series.to_frame : Convert Series to DataFrame.

        Examples
        --------
        >>> idx = pd.Index(['Ant', 'Bear', 'Cow'], name='animal')
        >>> idx.to_frame()
               animal
        animal
        Ant       Ant
        Bear     Bear
        Cow       Cow

        By default, the original Index is reused. To enforce a new Index:

        >>> idx.to_frame(index=False)
            animal
        0   Ant
        1  Bear
        2   Cow

        To override the name of the resulting column, specify `name`:

        >>> idx.to_frame(index=False, name='zoo')
            zoo
        0   Ant
        1  Bear
        2   Cow
        """
        from pandas import DataFrame

        if name is None:
            warnings.warn(
                "Explicitly passing `name=None` currently preserves the Index's name "
                "or uses a default name of 0. This behaviour is deprecated, and in "
                "the future `None` will be used as the name of the resulting "
                "DataFrame column.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            name = lib.no_default

        if name is lib.no_default:
            name = self.name or 0
        result = DataFrame({name: self._values.copy()})

        if index:
            result.index = self
        return result
