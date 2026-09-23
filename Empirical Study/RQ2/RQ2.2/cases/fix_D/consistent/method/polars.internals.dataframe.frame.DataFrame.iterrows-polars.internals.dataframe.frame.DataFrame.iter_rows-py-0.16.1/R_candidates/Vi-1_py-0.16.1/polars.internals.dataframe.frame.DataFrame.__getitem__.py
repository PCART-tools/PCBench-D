    def __getitem__(
        self,
        item: (
            str
            | int
            | np.ndarray[Any, Any]
            | MultiColSelector
            | tuple[int, MultiColSelector]
            | tuple[MultiRowSelector, MultiColSelector]
            | tuple[MultiRowSelector, int]
            | tuple[MultiRowSelector, str]
            | tuple[int, int]
            | tuple[int, str]
        ),
    ) -> DataFrame | pli.Series:
        """Get item. Does quite a lot. Read the comments."""
        # select rows and columns at once
        # every 2d selection, i.e. tuple is row column order, just like numpy
        if isinstance(item, tuple) and len(item) == 2:
            row_selection, col_selection = item

            # df[:, unknown]
            if isinstance(row_selection, slice):

                # multiple slices
                # df[:, :]
                if isinstance(col_selection, slice):
                    # slice can be
                    # by index
                    #   [1:8]
                    # or by column name
                    #   ["foo":"bar"]
                    # first we make sure that the slice is by index
                    start = col_selection.start
                    stop = col_selection.stop
                    if isinstance(col_selection.start, str):
                        start = self.find_idx_by_name(col_selection.start)
                    if isinstance(col_selection.stop, str):
                        stop = self.find_idx_by_name(col_selection.stop) + 1

                    col_selection = slice(start, stop, col_selection.step)

                    df = self.__getitem__(self.columns[col_selection])
                    return df[row_selection]

                # df[:, [True, False]]
                if is_bool_sequence(col_selection) or (
                    isinstance(col_selection, pli.Series)
                    and col_selection.dtype == Boolean
                ):
                    if len(col_selection) != self.width:
                        raise ValueError(
                            f"Expected {self.width} values when selecting columns by"
                            f" boolean mask. Got {len(col_selection)}."
                        )
                    series_list = []
                    for (i, val) in enumerate(col_selection):
                        if val:
                            series_list.append(self.to_series(i))

                    df = self.__class__(series_list)
                    return df[row_selection]

            # df[2, :] (select row as df)
            if isinstance(row_selection, int):
                if isinstance(col_selection, (slice, list)) or (
                    _check_for_numpy(col_selection)
                    and isinstance(col_selection, np.ndarray)
                ):
                    df = self[:, col_selection]
                    return df.slice(row_selection, 1)
                # df[2, "a"]
                if isinstance(col_selection, str):
                    return self[col_selection][row_selection]

            # column selection can be "a" and ["a", "b"]
            if isinstance(col_selection, str):
                col_selection = [col_selection]

            # df[:, 1]
            if isinstance(col_selection, int):
                series = self.to_series(col_selection)
                return series[row_selection]

            if isinstance(col_selection, list):
                # df[:, [1, 2]]
                if is_int_sequence(col_selection):
                    series_list = [self.to_series(i) for i in col_selection]
                    df = self.__class__(series_list)
                    return df[row_selection]

            df = self.__getitem__(col_selection)
            return df.__getitem__(row_selection)

        # select single column
        # df["foo"]
        if isinstance(item, str):
            return pli.wrap_s(self._df.column(item))

        # df[idx]
        if isinstance(item, int):
            return self.slice(self._pos_idx(item, dim=0), 1)

        # df[range(n)]
        if isinstance(item, range):
            return self[range_to_slice(item)]

        # df[:]
        if isinstance(item, slice):
            return PolarsSlice(self).apply(item)

        # select rows by numpy mask or index
        # df[np.array([1, 2, 3])]
        # df[np.array([True, False, True])]
        if _check_for_numpy(item) and isinstance(item, np.ndarray):
            if item.ndim != 1:
                raise ValueError("Only a 1D-Numpy array is supported as index.")
            if item.dtype.kind in ("i", "u"):
                # Numpy array with signed or unsigned integers.
                return self._from_pydf(
                    self._df.take_with_series(self._pos_idxs(item, dim=0)._s)
                )
            if isinstance(item[0], str):
                return self._from_pydf(self._df.select(item))

        if is_str_sequence(item, allow_str=False):
            # select multiple columns
            # df[["foo", "bar"]]
            return self._from_pydf(self._df.select(item))
        elif is_int_sequence(item):
            item = pli.Series("", item)  # fall through to next if isinstance

        if isinstance(item, pli.Series):
            dtype = item.dtype
            if dtype == Utf8:
                return self._from_pydf(self._df.select(item))
            if dtype == UInt32:
                return self._from_pydf(self._df.take_with_series(item._s))
            if dtype in {UInt8, UInt16, UInt64, Int8, Int16, Int32, Int64}:
                return self._from_pydf(
                    self._df.take_with_series(self._pos_idxs(item, dim=0)._s)
                )

        # if no data has been returned, the operation is not supported
        raise ValueError(
            f"Cannot __getitem__ on DataFrame with item: '{item}'"
            f" of type: '{type(item)}'."
        )
