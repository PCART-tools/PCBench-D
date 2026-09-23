    @final
    def __iter__(self) -> Iterator[tuple[Hashable, NDFrameT]]:
        """
        Groupby iterator.

        Returns
        -------
        Generator yielding sequence of (name, subsetted object)
        for each group

        Examples
        --------

        For SeriesGroupBy:

        >>> lst = ['a', 'a', 'b']
        >>> ser = pd.Series([1, 2, 3], index=lst)
        >>> ser
        a    1
        a    2
        b    3
        dtype: int64
        >>> for x, y in ser.groupby(level=0):
        ...     print(f'{x}\\n{y}\\n')
        a
        a    1
        a    2
        dtype: int64
        b
        b    3
        dtype: int64

        For DataFrameGroupBy:

        >>> data = [[1, 2, 3], [1, 5, 6], [7, 8, 9]]
        >>> df = pd.DataFrame(data, columns=["a", "b", "c"])
        >>> df
           a  b  c
        0  1  2  3
        1  1  5  6
        2  7  8  9
        >>> for x, y in df.groupby(by=["a"]):
        ...     print(f'{x}\\n{y}\\n')
        (1,)
           a  b  c
        0  1  2  3
        1  1  5  6
        (7,)
           a  b  c
        2  7  8  9

        For Resampler:

        >>> ser = pd.Series([1, 2, 3, 4], index=pd.DatetimeIndex(
        ...                 ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15']))
        >>> ser
        2023-01-01    1
        2023-01-15    2
        2023-02-01    3
        2023-02-15    4
        dtype: int64
        >>> for x, y in ser.resample('MS'):
        ...     print(f'{x}\\n{y}\\n')
        2023-01-01 00:00:00
        2023-01-01    1
        2023-01-15    2
        dtype: int64
        2023-02-01 00:00:00
        2023-02-01    3
        2023-02-15    4
        dtype: int64
        """
        keys = self.keys
        level = self.level
        result = self.grouper.get_iterator(self._selected_obj, axis=self.axis)
        # error: Argument 1 to "len" has incompatible type "Hashable"; expected "Sized"
        if is_list_like(level) and len(level) == 1:  # type: ignore[arg-type]
            # GH 51583
            warnings.warn(
                "Creating a Groupby object with a length-1 list-like "
                "level parameter will yield indexes as tuples in a future version. "
                "To keep indexes as scalars, create Groupby objects with "
                "a scalar level parameter instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        if isinstance(keys, list) and len(keys) == 1:
            # GH#42795 - when keys is a list, return tuples even when length is 1
            result = (((key,), group) for key, group in result)
        return result
