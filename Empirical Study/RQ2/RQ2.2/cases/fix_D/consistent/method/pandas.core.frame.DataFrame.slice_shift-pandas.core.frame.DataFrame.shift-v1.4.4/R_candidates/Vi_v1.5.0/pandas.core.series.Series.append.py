    def append(
        self, to_append, ignore_index: bool = False, verify_integrity: bool = False
    ) -> Series:
        """
        Concatenate two or more Series.

        .. deprecated:: 1.4.0
            Use :func:`concat` instead. For further details see
            :ref:`whatsnew_140.deprecations.frame_series_append`

        Parameters
        ----------
        to_append : Series or list/tuple of Series
            Series to append with self.
        ignore_index : bool, default False
            If True, the resulting axis will be labeled 0, 1, …, n - 1.
        verify_integrity : bool, default False
            If True, raise Exception on creating index with duplicates.

        Returns
        -------
        Series
            Concatenated Series.

        See Also
        --------
        concat : General function to concatenate DataFrame or Series objects.

        Notes
        -----
        Iteratively appending to a Series can be more computationally intensive
        than a single concatenate. A better solution is to append values to a
        list and then concatenate the list with the original Series all at
        once.

        Examples
        --------
        >>> s1 = pd.Series([1, 2, 3])
        >>> s2 = pd.Series([4, 5, 6])
        >>> s3 = pd.Series([4, 5, 6], index=[3, 4, 5])
        >>> s1.append(s2)
        0    1
        1    2
        2    3
        0    4
        1    5
        2    6
        dtype: int64

        >>> s1.append(s3)
        0    1
        1    2
        2    3
        3    4
        4    5
        5    6
        dtype: int64

        With `ignore_index` set to True:

        >>> s1.append(s2, ignore_index=True)
        0    1
        1    2
        2    3
        3    4
        4    5
        5    6
        dtype: int64

        With `verify_integrity` set to True:

        >>> s1.append(s2, verify_integrity=True)
        Traceback (most recent call last):
        ...
        ValueError: Indexes have overlapping values: [0, 1, 2]
        """
        warnings.warn(
            "The series.append method is deprecated "
            "and will be removed from pandas in a future version. "
            "Use pandas.concat instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )

        return self._append(to_append, ignore_index, verify_integrity)
