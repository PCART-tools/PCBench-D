    @final
    @doc(position="first", klass=_shared_doc_kwargs["klass"])
    def first_valid_index(self) -> Hashable | None:
        """
        Return index for {position} non-NA value or None, if no non-NA value is found.

        Returns
        -------
        type of index

        Notes
        -----
        If all elements are non-NA/null, returns None.
        Also returns None for empty {klass}.

        Examples
        --------
        For Series:

        >>> s = pd.Series([None, 3, 4])
        >>> s.first_valid_index()
        1
        >>> s.last_valid_index()
        2

        For DataFrame:

        >>> df = pd.DataFrame({{'A': [None, None, 2], 'B': [None, 3, 4]}})
        >>> df
             A      B
        0  NaN    NaN
        1  NaN    3.0
        2  2.0    4.0
        >>> df.first_valid_index()
        1
        >>> df.last_valid_index()
        2
        """
        return self._find_valid_index(how="first")
