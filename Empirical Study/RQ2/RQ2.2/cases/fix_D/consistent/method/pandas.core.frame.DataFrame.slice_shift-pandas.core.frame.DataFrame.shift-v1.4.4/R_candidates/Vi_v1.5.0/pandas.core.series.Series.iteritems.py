    def iteritems(self) -> Iterable[tuple[Hashable, Any]]:
        """
        Lazily iterate over (index, value) tuples.

        .. deprecated:: 1.5.0
            iteritems is deprecated and will be removed in a future version.
            Use .items instead.

        This method returns an iterable tuple (index, value). This is
        convenient if you want to create a lazy iterator.

        Returns
        -------
        iterable
            Iterable of tuples containing the (index, value) pairs from a
            Series.

        See Also
        --------
        Series.items : Recommended alternative.
        DataFrame.items : Iterate over (column name, Series) pairs.
        DataFrame.iterrows : Iterate over DataFrame rows as (index, Series) pairs.
        """
        warnings.warn(
            "iteritems is deprecated and will be removed in a future version. "
            "Use .items instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self.items()
